## Feedback Received

### Staff Feedback

- Add more detail about post-MVP features beyond Assignment 2 functionality.
- Specify deployment target.
- Consider PostgreSQL for deployment instead of SQLite.
- Improve authentication security.
- Add concrete API cost ceilings and guardrails.

### Review Day Feedback

#### Suggested Features

- Receipt filtering/search
- Budgeting insights
- Recurring purchase detection
- Smarter category suggestions
- Trend charts and additional spending analytics

#### Suggested Improvements

- Add loading indicator while receipts are being processed
- Allow users to delete receipts
- Detect invalid uploads and non-receipt files
- Improve receipt editing workflow

---

## Planned Response

### Implemented

#### Loading Indicator
- Added upload loading state so users receive immediate feedback while receipt processing is running.
- Prevents confusion during OpenAI processing latency.

#### Receipt Deletion
- Added receipt deletion functionality.
- Users can permanently remove receipts from receipt history.

#### Receipt Search
- Added receipt search/filtering.
- Users can quickly find receipts by merchant name.

#### Smart Category Suggestions
- Added automatic category assignment through GPT-4.1 Vision extraction.
- Users no longer need to manually categorize every item.

#### Non-Receipt Detection
- Added LLM-based receipt validation.
- Rejects images that are not receipts before processing.

#### Budgeting Insights
- Added automatic spending insights and budget recommendations.
- Provides users with personalized spending summaries.

#### Improved Receipt Editing
- Added ability to create new receipt items after extraction.
- Allows correction of missing items from OCR/LLM extraction.

### Partially Implemented

#### Trend Charts
- Existing spending dashboard and category summaries provide spending visualization.
- Additional historical trend analysis remains future work.

### Deferred

#### Recurring Purchases
- Not implemented due to project timeline constraints.
- Identified as a strong future enhancement.

---

## Outcome

The final project addresses the major review-day usability concerns while significantly expanding functionality beyond the initial submission through:
- Search
- Budgeting insights
- Smart categorization
- Receipt validation
- Receipt deletion
- Loading feedback
- Improved editing workflow