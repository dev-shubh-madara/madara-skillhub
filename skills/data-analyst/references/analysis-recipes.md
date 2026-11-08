# Analysis recipes

## Inspect

```python
import pandas as pd
df = pd.read_csv(path)            # or pd.read_excel(path, sheet_name=None) to see every sheet
print(df.shape)
print(df.dtypes)
print(df.isna().sum().sort_values(ascending=False).head(15))
print(df.duplicated().sum(), "exact duplicate rows")
print(df.describe(include="all").T.head(30))
```

## Clean (write down each step)

```python
clean = df.copy()
clean.columns = clean.columns.str.strip().str.lower().str.replace(r"\W+", "_", regex=True)
clean["date"] = pd.to_datetime(clean["date"], errors="coerce", dayfirst=True)   # say which format you assumed
clean["amount"] = pd.to_numeric(clean["amount"].astype(str).str.replace(r"[^\d.\-]", "", regex=True), errors="coerce")
before = len(clean)
clean = clean.drop_duplicates()
print(before - len(clean), "duplicates removed")
clean.to_csv("cleaned.csv", index=False)
```

Count how many values became missing after each conversion. If it is more than a few, show examples and ask before dropping them.

## Sanity checks before you report

- Totals after cleaning match the raw totals, or the difference is explained.
- Dates fall in a plausible range. Check the min and max.
- Group counts add up to the row count.
- Percentages are computed on the right base, and that base is stated.

## Pick the chart

| Question | Chart |
|---|---|
| Change over time | Line (bar if few periods) |
| Compare categories | Horizontal bar, sorted |
| Part of a whole | Stacked bar or a simple table; pie only for 2 to 4 parts |
| Relationship between two numbers | Scatter |
| Distribution | Histogram or box plot |

Bars start at zero. Title states the finding ("Sales fell 18% after March"), not the axis names.

## Report template

```
Main finding: one sentence with the number.
Supporting numbers: three bullets at most.
What changed in the data: rows removed, assumptions made.
Limits: sample size, missing data, what this cannot prove.
Next question worth checking: one line.
```
