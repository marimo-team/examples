# A short workshop: can these prices be compared?

Suggested duration: 15 to 20 minutes. The interactive notebook and every record in it are synthetic. Participants need no account, API key, payment or live dataset. This is an exercise in data quality and observation design.

## 1. Inspect the contract before the number

Start with the default **Different point / line** scenario. Ask participants what they would lose by keeping only the price column. Compare the event, market, named outcome, point, period and settlement fields.

Change to **Same contract**. The verdict now establishes comparability only under the lesson's declared assumptions. Change to **Different settlement rules**, then **Unknown settlement rules**. A known mismatch and missing information both prevent this model from establishing comparability.

## 2. Separate source time from retrieval time

Return to **Same contract**. Raise B's source age to 6 minutes while keeping the default age and time-gap limits. Both records were retrieved at 12:00, but the source-age and time-gap checks now fail. Ask why fetching an old record again does not make its source timestamp current.

Select **Missing source timestamp**, then **Future source timestamp**. Unknown or inconsistent time is not evidence of freshness. Finally, select **Duplicate candidate records**. Both candidate prices remain visible and unresolved.

## 3. Count the observations you are choosing

Use a 15-minute polling interval, 8 active hours each day and 30 study days. The model makes 960 requests, leaves 16 hours unobserved each day, and assigns 2,880 hypothetical credits at a weight of 3.

Change to one-minute polling for 24 hours each day. Over the same 30 days, the model makes 43,200 requests. That is 45 times as many requests with a different observation schedule. It is not equivalent coverage at two prices.

Change only the hypothetical credit weight. The request count stays fixed. The weight is a teaching input, not any provider's billing rule.

## Discuss before adapting

- Which fields would your actual data source require to establish event and contract identity?
- What can you conclude when settlement terms or source timestamps are missing?
- What changes could occur between polls or outside the active window?
- How would caching, pagination, retries and provider refresh delays change the workload model?

The lesson's checks are deliberately small and do not constitute a production normalizer or recommend wagers. Keep any later real-data adaptation private and respect its source rights. The MIT license covers this teaching code and synthetic examples; it grants no rights to redistribute an API provider's data.

Prepared by Astra, an AI assistant working with the ParlayAPI team.
