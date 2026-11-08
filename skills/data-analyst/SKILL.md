---
name: data-analyst
description: Cleans, analyzes and visualizes data from CSV, Excel or JSON files and explains the findings in plain language. Use when the user shares a spreadsheet or dataset, asks for trends, charts, summaries, or wants to know what the numbers say.
---

# Data analyst

## Before you start

Ask what decision the data should help with. Look at the file before assuming anything: columns, types, row count, missing values.

## Workflow

1. **Inspect.** Shape, column types, missing values, duplicates, odd values. Report what you find in a few lines.
2. **Clean.** Fix types and dates, handle missing values in a stated way, remove exact duplicates. Keep the raw file untouched and write the cleaned copy next to it. List every change made.
3. **Question first.** Turn the user's goal into two or three specific questions, then compute the answers in code. Do not estimate numbers by eye or in prose.
4. **Analyze.** Summary statistics, group comparisons, trends over time, and outliers, as the questions need.
5. **Chart.** One chart per message: pick the chart that fits the data (line for time, bar for categories, scatter for relationships). Label axes with units and give each chart a title that states the finding.
6. **Explain.** Lead with the main result, then the supporting numbers, then limits: small samples, missing data, correlation not proving cause.
7. **Hand over** the cleaned data and the script, so the work can be repeated.

## Quality bar

- Every number in the summary comes from code that ran.
- Totals are cross-checked against the raw data.
- Assumptions are written down.
- The summary can be understood by someone who never opens the file.

## Avoid

- Dropping rows silently.
- Charts with truncated axes that exaggerate a small change.
- Claiming causes the data cannot show.
- Overwriting the user's original file.
