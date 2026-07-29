---
name: proven-cash-yield
description: Calculate and quality-rank Proven Cash Yield (PCY), a three-year owner-cash valuation metric based only on qualified SEC facts and synchronized Massive market data. Use when the user asks for a factual or cash-based alternative to P/E, a company's PCY, owner-cash yield or multiple, US-wide or sector-relative value indices, parity prices, or rankings of US companies by demonstrated cash generation.
---

# Proven Cash Yield

Use the bundled calculator for every result. Do not reproduce the calculation
manually or replace missing data with estimates.

```sh
{skill_path}/scripts/proven-cash-yield company AAPL
{skill_path}/scripts/proven-cash-yield rank --universe major-exchanges --sort pcy --limit 25
{skill_path}/scripts/proven-cash-yield rank --universe us-common --sort sector-index --limit 50
```

Map "all US companies/common stocks" to `us-common`. Use `major-exchanges`
unless the user explicitly includes OTC listings. Sort by `pcy` unless the user
asks for sector-adjusted or relative ranking, then use `sector-index`.

The launcher reads `massive_api_key` and `sec_user_agent` from chezmoi data and
passes them only to the calculator process. If either value is missing, stop
and relay the launcher's exact remediation.

## Present results

For one company, report:

- synchronized closing price, price date, and reconciled market capitalization
- the three annual owner-cash inputs and their average
- PCY and Proven Cash Multiple
- US and FF12-sector medians, value indices, parity prices, and differences
- filing age, positive owner-cash year count, concentration warning, latest
  debt/cash, net-debt ratio, and diluted-share trend when available
- coverage or exclusion reason

For rankings, include only qualified companies. Show the requested leading rows
plus market price date, universe size, eligible count, each exclusion count,
benchmark sample sizes, and as-of timestamp.

Always state:

- Higher positive PCY and Value Index indicate more historical cash support at
  the observed price.
- Parity Price is the price that would match the selected cohort's median PCY.
- PCY is a historical relative-valuation metric, not intrinsic value, a price
  target, a forecast, or investment advice.

Do not calculate PCY for FF12 `Money` companies. Do not show a multiple, value
index, or parity price for non-positive PCY.

Treat exclusion as a result, not an invitation to estimate missing values.
Explain stale filings, nonconsecutive fiscal periods, inconsistent market
capitalization, and nonrepeatable owner cash from the calculator output.

Use the Massive MCP server to resolve ambiguous company names and spot-check
the displayed ticker price/details. Start with `search_endpoints`, then call
the documented endpoint. If the MCP and calculator timestamps differ, disclose
the difference rather than silently mixing observations.

Read [references/methodology.md](references/methodology.md) when explaining,
auditing, or changing the calculation.
