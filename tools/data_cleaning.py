from pathlib import Path

import pandas as pd
from crewai.tools import BaseTool
from pydantic import BaseModel

from cleaning import clean_dataset, create_quality_report


class NoInput(BaseModel):
    pass


class DataCleaningTool(BaseTool):
    name: str = "data_cleaning"
    description: str = (
        "Clean sales_data.csv using deterministic Pandas rules. "
        "Create cleaned_sales_data.csv and cleaning_report.md. "
        "This tool requires no parameters."
    )
    args_schema: type[BaseModel] = NoInput

    def _run(self) -> str:
        input_file = Path("sales_data.csv")
        output_file = Path("cleaned_sales_data.csv")
        report_file = Path("cleaning_report.md")

        if not input_file.exists():
            return "Error: sales_data.csv was not found."

        original_data = pd.read_csv(input_file)
        cleaned_data = clean_dataset(original_data)

        cleaned_data.to_csv(
            output_file,
            index=False,
            encoding="utf-8-sig"
        )

        report = create_quality_report(
            original_data,
            cleaned_data
        )

        invalid_dates = (
            pd.to_datetime(
                original_data["order_date"],
                errors="coerce"
            ).isna()
            & original_data["order_date"].notna()
        )

        report_text = f"""# Data Doctor Cleaning Report

## Dataset summary

- Original rows: {report["original_rows"]}
- Cleaned rows: {report["cleaned_rows"]}
- Removed duplicate rows: {report["removed_rows"]}
- Missing values before cleaning: {report["original_missing_values"]}
- Missing values after cleaning: {report["cleaned_missing_values"]}
- Duplicate rows before cleaning: {report["original_duplicates"]}
- Duplicate rows after cleaning: {report["cleaned_duplicates"]}

## Verified cleaning actions

1. Removed exact duplicate rows.
2. Filled missing numeric values using the median.
3. Replaced invalid ages using the median valid age.
4. Standardized customer names and city capitalization.
5. Replaced missing city values with `Unknown`.
6. Converted invalid dates to missing date values.
7. Preserved the order amount outlier `12000` for human review.

## Invalid dates detected

- Count: {int(invalid_dates.sum())}

## Output files

- `cleaned_sales_data.csv`
- `cleaning_report.md`
"""

        report_file.write_text(
            report_text,
            encoding="utf-8"
        )

        return report_text


tools = [
    DataCleaningTool()
]