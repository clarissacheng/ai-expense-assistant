# Regrets

## What I Would Improve or Add

- A geographical map of prices at several different locations across a certain region would be a really sick feature
- Add recurring subscription detection
- Add OCR confidence scores
- Add receipt image storage

## Lessons Learned

- Deploying authentication took longer than expected
- Database migrations should have been planned earlier
- Building incrementally from Assignment 2 saved significant time

## Features We Wanted To Implement

### Recurring Purchase Detection

We planned to automatically detect subscriptions and recurring purchases using merchant history and spending patterns. We were unable to complete this feature due to time constraints.

### Advanced Trend Analytics

We wanted to build monthly spending trends, forecasting, and richer visualizations. The current dashboard provides summaries and category breakdowns but does not yet support long-term trend analysis.

## What We Learned

- Defining API contracts early would have reduced frontend/backend integration time.
- Authentication and deployment took longer than expected.
- Building user-facing polish features (loading states, validation, editing workflows) significantly improved usability.
- GPT-based extraction works well but always requires correction workflows for real-world usage.

## Advice For Future Engineers

- Build editing and correction flows early.
- Add validation before integrating expensive LLM calls.
- Design deployment and database architecture before implementation begins.
- Leave extra time for deployment and debugging.