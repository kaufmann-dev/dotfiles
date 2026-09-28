#!/usr/bin/env python3
"""Calculate Proven Cash Yield from SEC facts and Massive market data."""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import json
import os
import statistics
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path
from typing import Any, Iterable
from zoneinfo import ZoneInfo


MASSIVE_BASE = "https://api.massive.com"
SEC_COMPANYFACTS_ZIP = (
    "https://www.sec.gov/Archives/edgar/daily-index/xbrl/companyfacts.zip"
)
SEC_SUBMISSIONS_ZIP = (
    "https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip"
)
MAJOR_EXCHANGES = {"XNAS", "XNYS", "XASE"}
DETAIL_TTL_SECONDS = 7 * 24 * 60 * 60
BULK_TTL_SECONDS = 24 * 60 * 60
MIN_SECTOR_SAMPLE = 10
MAX_FISCAL_DATA_AGE_DAYS = 500
MARKET_DATE_LOOKBACK_DAYS = 8
MARKET_CAP_RECONCILIATION_TOLERANCE = 0.10
OWNER_CASH_CONCENTRATION_THRESHOLD = 0.70
MARKET_CLOSE_READY_HOUR_ET = 18

OCF_TAGS = (
    "NetCashProvidedByUsedInOperatingActivities",
    "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations",
)
CAPEX_TAGS = (
    "PaymentsToAcquirePropertyPlantAndEquipment",
    "PaymentsToAcquireProductiveAssets",
)
SBC_TAGS = (
    "ShareBasedCompensation",
    "EmployeeServiceShareBasedCompensationNoncash",
)
DILUTED_SHARE_TAGS = ("WeightedAverageNumberOfDilutedSharesOutstanding",)
CASH_TAGS = (
    "CashAndCashEquivalentsAtCarryingValue",
    "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents",
)
TOTAL_DEBT_TAGS = (
    "LongTermDebtAndFinanceLeaseObligations",
    "LongTermDebt",
)
CURRENT_DEBT_TAGS = (
    "LongTermDebtAndFinanceLeaseObligationsCurrent",
    "LongTermDebtCurrent",
)
NONCURRENT_DEBT_TAGS = (
    "LongTermDebtNoncurrent",
)

# Fama-French 12-industry definitions, expressed as inclusive SIC ranges.
FF12_RANGES: tuple[tuple[str, tuple[tuple[int, int], ...]], ...] = (
    ("NoDur", ((100, 999), (2000, 2399), (2700, 2749), (2770, 2799), (3100, 3199), (3940, 3989))),
    ("Durbl", ((2500, 2519), (2590, 2599), (3630, 3659), (3710, 3711), (3714, 3714), (3716, 3716), (3750, 3751), (3792, 3792), (3900, 3939), (3990, 3999))),
    ("Manuf", ((2520, 2589), (2600, 2699), (2750, 2769), (3000, 3099), (3200, 3569), (3580, 3629), (3700, 3709), (3712, 3713), (3715, 3715), (3717, 3749), (3752, 3791), (3793, 3799), (3830, 3839), (3860, 3899))),
    ("Enrgy", ((1200, 1399), (2900, 2999))),
    ("Chems", ((2800, 2829), (2840, 2899))),
    ("BusEq", ((3570, 3579), (3660, 3692), (3694, 3699), (3810, 3829), (7370, 7379))),
    ("Telcm", ((4800, 4899),)),
    ("Utils", ((4900, 4949),)),
    ("Shops", ((5000, 5999), (7200, 7299), (7600, 7699))),
    ("Hlth", ((2830, 2839), (3693, 3693), (3840, 3859), (8000, 8099))),
    ("Money", ((6000, 6999),)),
)


class DataError(RuntimeError):
    """Expected source data is unavailable or ambiguous."""


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def iso_now() -> str:
    return utc_now().isoformat()


def ff12_sector(sic: str | int | None) -> str:
    try:
        code = int(str(sic))
    except (TypeError, ValueError):
        return "Unknown"
    for name, ranges in FF12_RANGES:
        if any(start <= code <= end for start, end in ranges):
            return name
    return "Other"


def annual_series(
    companyfacts: dict[str, Any],
    tags: Iterable[str],
    unit: str,
    as_of_date: dt.date,
) -> dict[str, float]:
    us_gaap = companyfacts.get("facts", {}).get("us-gaap", {})
    candidates: list[tuple[str, int, dict[str, float]]] = []
    for tag_index, tag in enumerate(tags):
        observations = us_gaap.get(tag, {}).get("units", {}).get(unit, [])
        selected: dict[str, dict[str, Any]] = {}
        for item in observations:
            if item.get("form") not in {"10-K", "10-K/A"} or item.get("fp") != "FY":
                continue
            start, end, filed = item.get("start"), item.get("end"), item.get("filed")
            if not start or not end or not filed or item.get("val") is None:
                continue
            try:
                duration = (dt.date.fromisoformat(end) - dt.date.fromisoformat(start)).days
                filed_date = dt.date.fromisoformat(filed)
            except ValueError:
                continue
            if not 300 <= duration <= 430 or filed_date > as_of_date:
                continue
            previous = selected.get(end)
            if previous is None or str(item.get("filed", "")) > str(previous.get("filed", "")):
                selected[end] = item
        if len(selected) >= 3:
            series = {end: float(item["val"]) for end, item in selected.items()}
            candidates.append((max(series), -tag_index, series))
    return max(candidates, default=("", 0, {}), key=lambda item: (item[0], item[1]))[2]


def latest_instant(
    companyfacts: dict[str, Any],
    tags: Iterable[str],
    as_of_date: dt.date,
) -> float | None:
    us_gaap = companyfacts.get("facts", {}).get("us-gaap", {})
    for tag in tags:
        observations = us_gaap.get(tag, {}).get("units", {}).get("USD", [])
        valid = []
        for item in observations:
            try:
                filed_date = dt.date.fromisoformat(str(item.get("filed", "")))
            except ValueError:
                continue
            if (
                item.get("form") in {"10-K", "10-K/A", "10-Q", "10-Q/A"}
                and item.get("end")
                and item.get("val") is not None
                and filed_date <= as_of_date
            ):
                valid.append(item)
        if valid:
            item = max(valid, key=lambda row: (str(row.get("end")), str(row.get("filed", ""))))
            return float(item["val"])
    return None


def latest_debt(companyfacts: dict[str, Any], as_of_date: dt.date) -> float | None:
    total = latest_instant(companyfacts, TOTAL_DEBT_TAGS, as_of_date)
    if total is not None:
        return total
    current = latest_instant(companyfacts, CURRENT_DEBT_TAGS, as_of_date)
    noncurrent = latest_instant(companyfacts, NONCURRENT_DEBT_TAGS, as_of_date)
    components = [value for value in (current, noncurrent) if value is not None]
    return sum(components) if components else None


def owner_cash_history(
    companyfacts: dict[str, Any],
    as_of_date: dt.date,
) -> tuple[list[dict[str, float | str]], str | None]:
    ocf = annual_series(companyfacts, OCF_TAGS, "USD", as_of_date)
    capex = annual_series(companyfacts, CAPEX_TAGS, "USD", as_of_date)
    sbc = annual_series(companyfacts, SBC_TAGS, "USD", as_of_date)
    common_ends = sorted(set(ocf) & set(capex) & set(sbc), reverse=True)
    if len(common_ends) < 3:
        return [], "fewer than three complete annual OCF/capex/stock-comp periods"
    selected_ends = common_ends[:3]
    period_dates = [dt.date.fromisoformat(end) for end in selected_ends]
    fiscal_age_days = (as_of_date - period_dates[0]).days
    if fiscal_age_days < 0 or fiscal_age_days > MAX_FISCAL_DATA_AGE_DAYS:
        return [], (
            f"stale annual financials: latest period is {fiscal_age_days} days old "
            f"(maximum {MAX_FISCAL_DATA_AGE_DAYS})"
        )
    gaps = [
        (newer - older).days
        for newer, older in zip(period_dates, period_dates[1:])
    ]
    if any(not 300 <= gap <= 430 for gap in gaps):
        return [], f"nonconsecutive annual periods: gaps are {gaps}"
    history: list[dict[str, float | str]] = []
    for end in selected_ends:
        if capex[end] < 0 or sbc[end] < 0:
            return [], f"ambiguous sign for capex or stock compensation in period {end}"
        owner_cash = ocf[end] - capex[end] - sbc[end]
        history.append(
            {
                "period_end": end,
                "operating_cash_flow": ocf[end],
                "capital_expenditure": capex[end],
                "stock_compensation": sbc[end],
                "owner_cash": owner_cash,
            }
        )
    return history, None


def owner_cash_quality(
    history: list[dict[str, float | str]],
) -> tuple[dict[str, float | int | bool], str | None]:
    values = [float(row["owner_cash"]) for row in history]
    positive_values = [value for value in values if value > 0]
    positive_years = len(positive_values)
    positive_total = sum(positive_values)
    largest_positive_year_share = (
        max(positive_values) / positive_total if positive_total > 0 else None
    )
    quality: dict[str, float | int | bool] = {
        "owner_cash_positive_years": positive_years,
        "owner_cash_concentration_warning": bool(
            largest_positive_year_share is not None
            and largest_positive_year_share > OWNER_CASH_CONCENTRATION_THRESHOLD
        ),
    }
    if largest_positive_year_share is not None:
        quality["owner_cash_largest_positive_year_share"] = largest_positive_year_share
    if values[0] <= 0:
        return quality, "nonpositive latest owner cash"
    if positive_years < 2:
        return quality, "fewer than two positive owner-cash years"
    return quality, None


def owner_cash_exclusion(error: str) -> str:
    if error.startswith("stale annual financials"):
        return "stale_financials"
    if error.startswith("nonconsecutive annual periods"):
        return "nonconsecutive_financials"
    return "incomplete_owner_cash"


def median_positive(values: Iterable[float]) -> float | None:
    positive = [value for value in values if value > 0]
    return statistics.median(positive) if positive else None


def price_from_daily_bar(row: dict[str, Any]) -> tuple[float | None, str | None]:
    value, timestamp = row.get("c"), row.get("t")
    if isinstance(value, (int, float)) and value > 0:
        return float(value), str(timestamp) if timestamp is not None else None
    return None, None


def dollar_volume(row: dict[str, Any]) -> float:
    price, _ = price_from_daily_bar(row)
    volume = row.get("v") or 0
    return (price or 0) * float(volume or 0)


def market_date_candidates(now: dt.datetime) -> list[dt.date]:
    eastern = now.astimezone(ZoneInfo("America/New_York"))
    first = eastern.date()
    if eastern.hour < MARKET_CLOSE_READY_HOUR_ET:
        first -= dt.timedelta(days=1)
    return [
        first - dt.timedelta(days=offset)
        for offset in range(MARKET_DATE_LOOKBACK_DAYS)
    ]


def reconciled_market_cap(
    price: float,
    detail: dict[str, Any],
) -> tuple[dict[str, float], str | None]:
    shares = detail.get("weighted_shares_outstanding")
    reported_market_cap = detail.get("market_cap")
    if not isinstance(shares, (int, float)) or shares <= 0:
        return {}, "missing weighted shares"
    if not isinstance(reported_market_cap, (int, float)) or reported_market_cap <= 0:
        return {}, "missing reported market capitalization"
    calculated_market_cap = price * float(shares)
    difference = abs(calculated_market_cap - float(reported_market_cap)) / float(
        reported_market_cap
    )
    if difference > MARKET_CAP_RECONCILIATION_TOLERANCE:
        return {}, (
            f"market capitalization differs by {difference:.2%} "
            f"(maximum {MARKET_CAP_RECONCILIATION_TOLERANCE:.0%})"
        )
    return {
        "weighted_shares_outstanding": float(shares),
        "reported_market_cap": float(reported_market_cap),
        "market_cap": calculated_market_cap,
        "market_cap_reconciliation_difference": difference,
    }, None


class JsonHttpClient:
    def __init__(self, user_agent: str, authorization: str | None = None) -> None:
        self.user_agent = user_agent
        self.authorization = authorization

    def request(self, url: str, attempts: int = 5) -> dict[str, Any]:
        headers = {"User-Agent": self.user_agent, "Accept": "application/json"}
        if self.authorization:
            headers["Authorization"] = f"Bearer {self.authorization}"
        for attempt in range(attempts):
            try:
                with urllib.request.urlopen(
                    urllib.request.Request(url, headers=headers), timeout=60
                ) as response:
                    return json.load(response)
            except urllib.error.HTTPError as exc:
                if exc.code not in {429, 500, 502, 503, 504} or attempt == attempts - 1:
                    raise DataError(f"HTTP {exc.code} from {urllib.parse.urlsplit(url).path}") from exc
                retry_after = exc.headers.get("Retry-After")
                delay = float(retry_after) if retry_after and retry_after.isdigit() else 2**attempt
                time.sleep(min(delay, 30))
            except (urllib.error.URLError, TimeoutError) as exc:
                if attempt == attempts - 1:
                    raise DataError(f"request failed for {urllib.parse.urlsplit(url).path}") from exc
                time.sleep(min(2**attempt, 30))
        raise AssertionError("unreachable")


class MassiveClient:
    def __init__(self, api_key: str) -> None:
        self.http = JsonHttpClient("proven-cash-yield/1", api_key)

    def get(self, path_or_url: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = path_or_url if path_or_url.startswith("http") else MASSIVE_BASE + path_or_url
        if params:
            url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
        return self.http.request(url)

    def universe(self) -> list[dict[str, Any]]:
        url = "/v3/reference/tickers"
        params: dict[str, Any] | None = {
            "market": "stocks",
            "type": "CS",
            "active": "true",
            "limit": 1000,
            "sort": "ticker",
        }
        rows: list[dict[str, Any]] = []
        while url:
            payload = self.get(url, params)
            rows.extend(payload.get("results", []))
            url = payload.get("next_url", "")
            params = None
        return rows

    def daily_market(
        self,
        date: dt.date,
        include_otc: bool,
    ) -> dict[str, dict[str, Any]]:
        payload = self.get(
            f"/v2/aggs/grouped/locale/us/market/stocks/{date.isoformat()}",
            {
                "adjusted": "true",
                "include_otc": str(include_otc).lower(),
            },
        )
        return {row["T"]: row for row in payload.get("results", []) if row.get("T")}

    def details(self, ticker: str, date: dt.date) -> dict[str, Any]:
        payload = self.get(
            f"/v3/reference/tickers/{urllib.parse.quote(ticker, safe='')}",
            {"date": date.isoformat()},
        )
        result = payload.get("results")
        if not isinstance(result, dict):
            raise DataError(f"Massive returned no ticker details for {ticker}")
        return result


class Cache:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.details_path = root / "massive-details.json"

    def fresh(self, path: Path, ttl: int) -> bool:
        return path.exists() and time.time() - path.stat().st_mtime < ttl

    def download(self, url: str, name: str, user_agent: str, refresh: bool) -> Path:
        path = self.root / name
        if not refresh and self.fresh(path, BULK_TTL_SECONDS):
            return path
        request = urllib.request.Request(url, headers={"User-Agent": user_agent})
        with urllib.request.urlopen(request, timeout=180) as response:
            with tempfile.NamedTemporaryFile(dir=self.root, delete=False) as handle:
                temp_path = Path(handle.name)
                while chunk := response.read(1024 * 1024):
                    handle.write(chunk)
        temp_path.replace(path)
        return path

    def load_details(self) -> dict[str, Any]:
        if not self.details_path.exists():
            return {}
        try:
            return json.loads(self.details_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}

    def save_details(self, data: dict[str, Any]) -> None:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=self.root, delete=False
        ) as handle:
            json.dump(data, handle, separators=(",", ":"))
            temp_path = Path(handle.name)
        temp_path.replace(self.details_path)


def zip_json(archive: zipfile.ZipFile, cik: str) -> dict[str, Any] | None:
    name = f"CIK{int(cik):010d}.json"
    try:
        with archive.open(name) as handle:
            return json.load(handle)
    except KeyError:
        return None


def fetch_details(
    client: MassiveClient,
    cache: Cache,
    tickers: list[str],
    market_date: dt.date,
    refresh: bool,
) -> dict[str, dict[str, Any]]:
    stored = cache.load_details()
    now = time.time()
    output: dict[str, dict[str, Any]] = {}
    missing: list[str] = []
    for ticker in tickers:
        cache_key = f"{ticker}@{market_date.isoformat()}"
        item = stored.get(cache_key)
        if (
            not refresh
            and isinstance(item, dict)
            and now - float(item.get("fetched_at", 0)) < DETAIL_TTL_SECONDS
        ):
            output[ticker] = item["data"]
        else:
            missing.append(ticker)

    def one(ticker: str) -> tuple[str, dict[str, Any] | None]:
        try:
            return ticker, client.details(ticker, market_date)
        except DataError:
            return ticker, None

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        for ticker, data in executor.map(one, missing):
            if data:
                output[ticker] = data
                cache_key = f"{ticker}@{market_date.isoformat()}"
                stored[cache_key] = {"fetched_at": now, "data": data}
    if missing:
        cache.save_details(stored)
    return output


def build_analysis(
    client: MassiveClient,
    cache: Cache,
    sec_user_agent: str,
    universe_name: str,
    refresh: bool,
) -> dict[str, Any]:
    as_of = utc_now()
    as_of_date = as_of.date()
    include_otc = universe_name == "us-common"
    universe = [
        row
        for row in client.universe()
        if row.get("cik")
        and (
            include_otc
            or row.get("primary_exchange") in MAJOR_EXCHANGES
        )
    ]
    market_date = None
    daily_bars: dict[str, dict[str, Any]] = {}
    for candidate_date in market_date_candidates(as_of):
        try:
            daily_bars = client.daily_market(candidate_date, include_otc)
        except DataError:
            continue
        if daily_bars:
            market_date = candidate_date
            break
    if market_date is None:
        raise DataError("Massive returned no completed US daily market session")

    by_cik: dict[str, list[dict[str, Any]]] = {}
    for row in universe:
        daily_bar = daily_bars.get(row["ticker"])
        price, _ = price_from_daily_bar(daily_bar or {})
        if price:
            row = dict(row)
            row["_daily_bar"] = daily_bar
            by_cik.setdefault(str(row["cik"]), []).append(row)

    representatives = {
        cik: max(rows, key=lambda row: dollar_volume(row["_daily_bar"]))
        for cik, rows in by_cik.items()
    }

    facts_path = cache.download(
        SEC_COMPANYFACTS_ZIP, "companyfacts.zip", sec_user_agent, refresh
    )
    submissions_path = cache.download(
        SEC_SUBMISSIONS_ZIP, "submissions.zip", sec_user_agent, refresh
    )

    candidates: list[dict[str, Any]] = []
    exclusions: dict[str, int] = {
        "financial_company": 0,
        "missing_sec_data": 0,
        "incomplete_owner_cash": 0,
        "missing_market_data": 0,
        "stale_financials": 0,
        "nonconsecutive_financials": 0,
        "nonpositive_latest_owner_cash": 0,
        "insufficient_positive_owner_cash": 0,
        "market_cap_mismatch": 0,
    }
    excluded_tickers: dict[str, str] = {}
    with zipfile.ZipFile(facts_path) as facts_zip, zipfile.ZipFile(submissions_path) as subs_zip:
        for cik, listing in representatives.items():
            facts = zip_json(facts_zip, cik)
            submission = zip_json(subs_zip, cik)
            if not facts or not submission:
                exclusions["missing_sec_data"] += 1
                excluded_tickers[listing["ticker"]] = "missing SEC data"
                continue
            sector = ff12_sector(submission.get("sic"))
            if sector == "Money":
                exclusions["financial_company"] += 1
                excluded_tickers[listing["ticker"]] = "unsupported financial company"
                continue
            history, error = owner_cash_history(facts, as_of_date)
            if error:
                reason = owner_cash_exclusion(error)
                exclusions[reason] += 1
                excluded_tickers[listing["ticker"]] = error
                continue
            quality, error = owner_cash_quality(history)
            if error:
                reason = (
                    "nonpositive_latest_owner_cash"
                    if error == "nonpositive latest owner cash"
                    else "insufficient_positive_owner_cash"
                )
                exclusions[reason] += 1
                excluded_tickers[listing["ticker"]] = error
                continue
            price, price_timestamp = price_from_daily_bar(listing["_daily_bar"])
            if not price:
                exclusions["missing_market_data"] += 1
                excluded_tickers[listing["ticker"]] = "missing completed-session price"
                continue
            avg_owner_cash = statistics.fmean(float(row["owner_cash"]) for row in history)
            diluted = annual_series(facts, DILUTED_SHARE_TAGS, "shares", as_of_date)
            diluted_values = [diluted[end] for end in sorted(diluted, reverse=True)[:3]]
            dilution_change = None
            if len(diluted_values) == 3 and diluted_values[-1] > 0:
                dilution_change = diluted_values[0] / diluted_values[-1] - 1
            candidates.append(
                {
                    "ticker": listing["ticker"],
                    "company": listing.get("name") or facts.get("entityName"),
                    "cik": f"{int(cik):010d}",
                    "exchange": listing.get("primary_exchange"),
                    "sic": str(submission.get("sic") or ""),
                    "sector": sector,
                    "price": price,
                    "price_timestamp": price_timestamp,
                    "price_date": market_date.isoformat(),
                    "price_age_days": (as_of_date - market_date).days,
                    "history": history,
                    "average_owner_cash": avg_owner_cash,
                    "fiscal_data_age_days": (
                        as_of_date
                        - dt.date.fromisoformat(str(history[0]["period_end"]))
                    ).days,
                    "cash": latest_instant(facts, CASH_TAGS, as_of_date),
                    "debt": latest_debt(facts, as_of_date),
                    "diluted_share_change_3y": dilution_change,
                    **quality,
                }
            )

    details = fetch_details(
        client,
        cache,
        [row["ticker"] for row in candidates],
        market_date,
        refresh,
    )
    results: list[dict[str, Any]] = []
    for row in candidates:
        detail = details.get(row["ticker"], {})
        market_cap_data, error = reconciled_market_cap(row["price"], detail)
        if error:
            reason = (
                "market_cap_mismatch"
                if error.startswith("market capitalization differs")
                else "missing_market_data"
            )
            exclusions[reason] += 1
            excluded_tickers[row["ticker"]] = error
            continue
        market_cap = market_cap_data["market_cap"]
        if market_cap <= 0:
            exclusions["missing_market_data"] += 1
            excluded_tickers[row["ticker"]] = "nonpositive market capitalization"
            continue
        pcy = row["average_owner_cash"] / market_cap
        net_debt = (
            row["debt"] - row["cash"]
            if row["debt"] is not None and row["cash"] is not None
            else None
        )
        row.update(
            {
                **market_cap_data,
                "pcy": pcy,
                "proven_cash_multiple": (1 / pcy) if pcy > 0 else None,
                "net_debt": net_debt,
                "net_debt_to_average_owner_cash": (
                    net_debt / row["average_owner_cash"]
                    if net_debt is not None and row["average_owner_cash"] > 0
                    else None
                ),
            }
        )
        results.append(row)

    us_median = median_positive(row["pcy"] for row in results)
    sector_values: dict[str, list[float]] = {}
    for row in results:
        if row["pcy"] > 0:
            sector_values.setdefault(row["sector"], []).append(row["pcy"])
    sector_medians = {
        sector: statistics.median(values)
        for sector, values in sector_values.items()
        if len(values) >= MIN_SECTOR_SAMPLE
    }

    for row in results:
        if row["pcy"] > 0 and us_median:
            row["us_value_index"] = row["pcy"] / us_median
            row["us_parity_price"] = row["price"] * row["us_value_index"]
            row["us_price_difference"] = row["us_value_index"] - 1
        else:
            row["us_value_index"] = row["us_parity_price"] = row["us_price_difference"] = None
        sector_median = sector_medians.get(row["sector"])
        row["sector_median_pcy"] = sector_median
        row["sector_sample_size"] = len(sector_values.get(row["sector"], []))
        if row["pcy"] > 0 and sector_median:
            row["sector_value_index"] = row["pcy"] / sector_median
            row["sector_parity_price"] = row["price"] * row["sector_value_index"]
            row["sector_price_difference"] = row["sector_value_index"] - 1
        else:
            row["sector_value_index"] = row["sector_parity_price"] = row["sector_price_difference"] = None

    pcy_order = sorted(results, key=lambda row: row["pcy"], reverse=True)
    for rank, row in enumerate(pcy_order, 1):
        row["pcy_rank"] = rank
        row["us_rank"] = rank
    sector_order = sorted(
        (row for row in results if row["sector_value_index"] is not None),
        key=lambda row: row["sector_value_index"],
        reverse=True,
    )
    for rank, row in enumerate(sector_order, 1):
        row["sector_rank"] = rank
    for row in results:
        row.setdefault("sector_rank", None)

    return {
        "as_of": as_of.isoformat(),
        "market_price_date": market_date.isoformat(),
        "universe": universe_name,
        "coverage": {
            "active_listings": len(universe),
            "unique_issuers_with_price": len(representatives),
            "eligible_companies": len(results),
            "positive_benchmark_companies": sum(row["pcy"] > 0 for row in results),
            "exclusions": exclusions,
        },
        "benchmarks": {
            "us_median_pcy": us_median,
            "us_sample_size": sum(row["pcy"] > 0 for row in results),
            "sector_medians": sector_medians,
        },
        "results": results,
        "_excluded_tickers": excluded_tickers,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
        / "proven-cash-yield",
    )
    parser.add_argument("--refresh", action="store_true")
    subparsers = parser.add_subparsers(dest="command", required=True)

    company = subparsers.add_parser("company", help="Analyze one company")
    company.add_argument("ticker", type=str.upper)
    company.add_argument(
        "--universe", choices=("major-exchanges", "us-common"), default="major-exchanges"
    )

    rank = subparsers.add_parser("rank", help="Rank eligible US companies")
    rank.add_argument(
        "--universe", choices=("major-exchanges", "us-common"), default="major-exchanges"
    )
    rank.add_argument(
        "--sort", choices=("pcy", "us-index", "sector-index"), default="pcy"
    )
    rank.add_argument("--limit", type=int, default=25)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    api_key = os.environ.get("MASSIVE_API_KEY", "")
    sec_user_agent = os.environ.get("SEC_USER_AGENT", "")
    if not api_key or not sec_user_agent:
        print(
            "MASSIVE_API_KEY and SEC_USER_AGENT must be provided by the scoped launcher.",
            file=sys.stderr,
        )
        return 2
    try:
        analysis = build_analysis(
            MassiveClient(api_key),
            Cache(args.cache_dir),
            sec_user_agent,
            args.universe,
            args.refresh,
        )
        if args.command == "company":
            ticker = args.ticker
            match = next(
                (row for row in analysis["results"] if row["ticker"] == ticker), None
            )
            if match is None:
                match = {
                    "ticker": ticker,
                    "qualified": False,
                    "exclusion_reason": analysis["_excluded_tickers"].get(
                        ticker,
                        "unsupported, unlisted, or not the representative share class",
                    ),
                }
            else:
                match["qualified"] = True
            output = {
                "as_of": analysis["as_of"],
                "market_price_date": analysis["market_price_date"],
                "universe": analysis["universe"],
                "coverage": analysis["coverage"],
                "benchmarks": analysis["benchmarks"],
                "company": match,
            }
        else:
            sort_key = {
                "pcy": "pcy",
                "us-index": "us_value_index",
                "sector-index": "sector_value_index",
            }[args.sort]
            ranked = sorted(
                analysis["results"],
                key=lambda row: (
                    row.get(sort_key) is not None,
                    row.get(sort_key) if row.get(sort_key) is not None else float("-inf"),
                ),
                reverse=True,
            )
            if args.limit > 0:
                ranked = ranked[: args.limit]
            output = {
                key: value
                for key, value in analysis.items()
                if key != "_excluded_tickers"
            }
            output.update({"sort": args.sort, "results": ranked})
        json.dump(output, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0
    except (DataError, OSError, zipfile.BadZipFile, json.JSONDecodeError) as exc:
        print(f"proven-cash-yield: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
