# Data Doctor Cleaning Report

## Dataset summary

- Original rows: 8
- Cleaned rows: 7
- Removed duplicate rows: 1
- Missing values before cleaning: 4
- Missing values after cleaning: 1
- Duplicate rows before cleaning: 1
- Duplicate rows after cleaning: 0

## Verified cleaning actions

1. Removed exact duplicate rows.
2. Filled missing numeric values using the median.
3. Replaced invalid ages using the median valid age.
4. Standardized customer names and city capitalization.
5. Replaced missing city values with `Unknown`.
6. Converted invalid dates to missing date values.
7. Preserved the order amount outlier `12000` for human review.

## Invalid dates detected

- Count: 1

## Output files

- `cleaned_sales_data.csv`
- `cleaning_report.md`
