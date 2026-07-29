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
) -> dict[str, float]:
    us_gaap = companyfacts.get("facts", {}).get("us-gaap", {})
    for tag in tags:
        observations = us_gaap.get(tag, {}).get("units", {}).get(unit, [])
        selected: dict[str, dict[str, Any]] = {}
        for item in observations:
            if item.get("form") not in {"10-K", "10-K/A"} or item.get("fp") != "FY":
                continue
            start, end = item.get("start"), item.get("end")
            if not start or not end or item.get("val") is None:
                continue
            try:
                duration = (dt.date.fromisoformat(end) - dt.date.fromisoformat(start)).days
            except ValueError:
                continue
            if not 300 <= duration <= 430:
                continue
            previous = selected.get(end)
            if previous is None or str(item.get("filed", "")) > str(previous.get("filed", "")):
                selected[end] = item
        if len(selected) >= 3:
            return {end: float(item["val"]) for end, item in selected.items()}
    return {}


def latest_instant(companyfacts: dict[str, Any], tags: Iterable[str]) -> float | None:
    us_gaap = companyfacts.get("facts", {}).get("us-gaap", {})
    for tag in tags:
        observations = us_gaap.get(tag, {}).get("units", {}).get("USD", [])
        valid = [
            item
            for item in observations
            if item.get("form") in {"10-K", "10-K/A", "10-Q", "10-Q/A"}
            and item.get("end")
            and item.get("val") is not None
        ]
        if valid:
            item = max(valid, key=lambda row: (str(row.get("end")), str(row.get("filed", ""))))
            return float(item["val"])
    return None


def latest_debt(companyfacts: dict[str, Any]) -> float | None:
    total = latest_instant(companyfacts, TOTAL_DEBT_TAGS)
    if total is not None:
        return total
    current = latest_instant(companyfacts, CURRENT_DEBT_TAGS)
    noncurrent = latest_instant(companyfacts, NONCURRENT_DEBT_TAGS)
    components = [value for value in (current, noncurrent) if value is not None]
    return sum(components) if components else None


def owner_cash_history(companyfacts: dict[str, Any]) -> tuple[list[dict[str, float | str]], str | None]:
    ocf = annual_series(companyfacts, OCF_TAGS, "USD")
    capex = annual_series(companyfacts, CAPEX_TAGS, "USD")
    sbc = annual_series(companyfacts, SBC_TAGS, "USD")
    common_ends = sorted(set(ocf) & set(capex) & set(sbc), reverse=True)
    if len(common_ends) < 3:
        return [], "fewer than three complete annual OCF/capex/stock-comp periods"
    history: list[dict[str, float | str]] = []
    for end in common_ends[:3]:
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


def median_positive(values: Iterable[float]) -> float | None:
    positive = [value for value in values if value > 0]
    return statistics.median(positive) if positive else None


def price_from_snapshot(row: dict[str, Any]) -> tuple[float | None, str | None]:
    candidates = (
        (row.get("lastTrade", {}).get("p"), row.get("lastTrade", {}).get("t")),
        (row.get("min", {}).get("c"), row.get("min", {}).get("t")),
        (row.get("day", {}).get("c"), row.get("updated")),
        (row.get("prevDay", {}).get("c"), row.get("updated")),
    )
    for value, timestamp in candidates:
        if isinstance(value, (int, float)) and value > 0:
            return float(value), str(timestamp) if timestamp is not None else None
    return None, None


def dollar_volume(row: dict[str, Any]) -> float:
    price, _ = price_from_snapshot(row)
    volume = row.get("day", {}).get("v") or row.get("prevDay", {}).get("v") or 0
    return (price or 0) * float(volume or 0)


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

    def snapshot(self, include_otc: bool) -> dict[str, dict[str, Any]]:
        payload = self.get(
            "/v2/snapshot/locale/us/markets/stocks/tickers",
            {"include_otc": str(include_otc).lower()},
        )
        return {row["ticker"]: row for row in payload.get("tickers", []) if row.get("ticker")}

    def details(self, ticker: str) -> dict[str, Any]:
        payload = self.get(f"/v3/reference/tickers/{urllib.parse.quote(ticker, safe='')}")
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
    refresh: bool,
) -> dict[str, dict[str, Any]]:
    stored = cache.load_details()
    now = time.time()
    output: dict[str, dict[str, Any]] = {}
    missing: list[str] = []
    for ticker in tickers:
        item = stored.get(ticker)
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
            return ticker, client.details(ticker)
        except DataError:
            return ticker, None

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        for ticker, data in executor.map(one, missing):
            if data:
                output[ticker] = data
                stored[ticker] = {"fetched_at": now, "data": data}
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
    snapshots = client.snapshot(include_otc)

    by_cik: dict[str, list[dict[str, Any]]] = {}
    for row in universe:
        snapshot = snapshots.get(row["ticker"])
        price, _ = price_from_snapshot(snapshot or {})
        if price:
            row = dict(row)
            row["_snapshot"] = snapshot
            by_cik.setdefault(str(row["cik"]), []).append(row)

    representatives = {
        cik: max(rows, key=lambda row: dollar_volume(row["_snapshot"]))
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
    }
    with zipfile.ZipFile(facts_path) as facts_zip, zipfile.ZipFile(submissions_path) as subs_zip:
        for cik, listing in representatives.items():
            facts = zip_json(facts_zip, cik)
            submission = zip_json(subs_zip, cik)
            if not facts or not submission:
                exclusions["missing_sec_data"] += 1
                continue
            sector = ff12_sector(submission.get("sic"))
            if sector == "Money":
                exclusions["financial_company"] += 1
                continue
            history, error = owner_cash_history(facts)
            if error:
                exclusions["incomplete_owner_cash"] += 1
                continue
            price, price_timestamp = price_from_snapshot(listing["_snapshot"])
            if not price:
                exclusions["missing_market_data"] += 1
                continue
            avg_owner_cash = statistics.fmean(float(row["owner_cash"]) for row in history)
            diluted = annual_series(facts, DILUTED_SHARE_TAGS, "shares")
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
                    "history": history,
                    "average_owner_cash": avg_owner_cash,
                    "cash": latest_instant(facts, CASH_TAGS),
                    "debt": latest_debt(facts),
                    "diluted_share_change_3y": dilution_change,
                }
            )

    details = fetch_details(client, cache, [row["ticker"] for row in candidates], refresh)
    results: list[dict[str, Any]] = []
    for row in candidates:
        detail = details.get(row["ticker"], {})
        shares = detail.get("weighted_shares_outstanding")
        if not isinstance(shares, (int, float)) or shares <= 0:
            exclusions["missing_market_data"] += 1
            continue
        market_cap = row["price"] * float(shares)
        pcy = row["average_owner_cash"] / market_cap
        row.update(
            {
                "weighted_shares_outstanding": float(shares),
                "market_cap": market_cap,
                "pcy": pcy,
                "proven_cash_multiple": (1 / pcy) if pcy > 0 else None,
                "net_debt": (
                    row["debt"] - row["cash"]
                    if row["debt"] is not None and row["cash"] is not None
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
        "as_of": iso_now(),
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
                raise DataError(
                    f"{ticker} is unsupported, excluded, or lacks three complete annual periods"
                )
            output = {
                "as_of": analysis["as_of"],
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
            output = {**analysis, "sort": args.sort, "results": ranked}
        json.dump(output, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0
    except (DataError, OSError, zipfile.BadZipFile, json.JSONDecodeError) as exc:
        print(f"proven-cash-yield: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
