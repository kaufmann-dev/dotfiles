# Proven Cash Yield Methodology

## Formula

For each of the latest three completed fiscal years:

```text
strict owner cash = operating cash flow - capital expenditure - stock compensation
```

```text
PCY = arithmetic mean(strict owner cash) / current market capitalization
Proven Cash Multiple = 1 / PCY
Value Index = company PCY / benchmark median PCY
Parity Price = current price * Value Index
Price Difference = Value Index - 1
```

For a ranking, use the adjusted closing price from Massive's latest completed
US market session for every company. Current market capitalization is that
price multiplied by Massive `weighted_shares_outstanding`. Require the result
to agree within 10% of Massive's reported market capitalization for the same
date. The share field treats other share classes as converted into the selected
representative class.

Use positive PCY observations only when calculating benchmark medians. Keep
non-positive PCY observations in raw rankings, below positive observations,
but report their multiple and relative values as not meaningful.

## SEC fact selection

Use facts from `us-gaap` with USD units:

- Operating cash flow: `NetCashProvidedByUsedInOperatingActivities`, then
  `NetCashProvidedByUsedInOperatingActivitiesContinuingOperations`.
- Capital expenditure: `PaymentsToAcquirePropertyPlantAndEquipment`, then
  `PaymentsToAcquireProductiveAssets`.
- Stock compensation: `ShareBasedCompensation`, then
  `EmployeeServiceShareBasedCompensationNoncash`.

For each concept, accept only 10-K or 10-K/A fiscal-year durations of 300 to
430 days filed by the analysis date. Group facts by period end and keep the
most recently filed value so amendments and later restatements supersede older
records. Prefer the tag with the freshest valid three-year series. Use the
latest three period ends common to all required concepts.

Require the latest fiscal period to be no more than 500 days old. Require each
adjacent fiscal period end to be 300 to 430 days apart. Reject missing or
negative capex and stock-compensation values rather than treating them as zero.

## Ranking qualification

Include a company in rankings only when:

- all three owner-cash periods pass the SEC freshness and consecutiveness rules
- latest owner cash is positive
- at least two of the three owner-cash years are positive
- a dated Massive closing price exists for the common completed market session
- closing price times weighted shares reconciles within 10% of Massive's
  reported market capitalization for the same date

Flag, but do not modify or exclude, owner cash when one year represents more
than 70% of the three years' total positive owner cash. Report filing age,
price age, positive owner-cash years, the concentration flag, market-cap
reconciliation difference, and net debt divided by average owner cash.

These thresholds qualify data for comparison; they do not change reported
facts or adjust the PCY value.

Debt, cash, and diluted shares are optional context and never change PCY.

## Universe and grouping

Use active Massive `CS` listings with a CIK. Deduplicate by CIK and choose the
listing with the highest current dollar volume. `major-exchanges` includes
`XNAS`, `XNYS`, and `XASE`; `us-common` also permits OTC listings.

Map the SEC four-digit SIC code to Fama-French 12 industries. Use the resulting
group as the sector benchmark. Mark the `Money` group unsupported because
operating cash flow and capital expenditure are not comparable valuation
inputs for financial firms.

Require at least ten positive eligible observations for a sector median.

## Interpretation

PCY measures how much strictly adjusted historical owner cash the company
generated relative to its current equity value. It uses no growth, discount
rate, terminal value, analyst estimate, or forecast.

The metric can still be distorted by cyclicality, working-capital movements,
acquisition accounting, unusually high or low capital expenditure, and the
accounting estimate used for stock compensation. Parity Price is a
benchmark-normalized observation, not fair value.
