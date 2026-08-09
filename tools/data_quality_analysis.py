import json
from pathlib import Path

import pandas as pd
from crewai.tools import BaseTool
from pydantic import BaseModel


class NoInput(BaseModel):
    pass


class DataQualityAnalysisTool(BaseTool):
    name: str = "data_quality_analysis"
    description: str = (
        "Analyze sales_data.csv using Pandas and return verified "
        "data-quality facts. This tool requires no parameters."
    )
    args_schema: type[BaseModel] = NoInput

    def _run(self) -> str:
        input_file = Path("sales_data.csv")

        if not input_file.exists():
            return "Error: sales_data.csv was not found."

        data = pd.read_csv(input_file)

        ages = pd.to_numeric(
            data["age"],
            errors="coerce"
        )

        invalid_age_mask = (
            ages.notna()
            & ((ages < 0) | (ages > 120))
        )

        dates = pd.to_datetime(
            data["order_date"],
            errors="coerce"
        )

        invalid_date_mask = (
            data["order_date"].notna()
            & dates.isna()
        )

        city_groups: dict[str, list[str]] = {}

        for city in data["city"].dropna().astype(str):
            normalized = city.strip().lower()
            city_groups.setdefault(normalized, [])

            if city not in city_groups[normalized]:
                city_groups[normalized].append(city)

        city_issues = {
            normalized: variants
            for normalized, variants in city_groups.items()
            if len(variants) > 1
        }

        amounts = pd.to_numeric(
            data["order_amount"],
            errors="coerce"
        )

        valid_amounts = amounts.dropna()

        q1 = valid_amounts.quantile(0.25)
        q3 = valid_amounts.quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)

        outlier_mask = (
            amounts.notna()
            & (
                (amounts < lower_bound)
                | (amounts > upper_bound)
            )
        )

        report = {
            "rows": int(data.shape[0]),
            "columns": int(data.shape[1]),
            "column_names": data.columns.tolist(),
            "data_types": data.dtypes.astype(str).to_dict(),
            "missing_values": (
                data.isnull()
                .sum()
                .astype(int)
                .to_dict()
            ),
            "total_missing_values": int(
                data.isnull().sum().sum()
            ),
            "duplicate_rows": int(
                data.duplicated().sum()
            ),
            "invalid_ages": (
                data.loc[invalid_age_mask]
                .to_dict(orient="records")
            ),
            "invalid_dates": (
                data.loc[invalid_date_mask]
                .to_dict(orient="records")
            ),
            "inconsistent_city_names": city_issues,
            "order_amount_outliers": (
                data.loc[outlier_mask]
                .to_dict(orient="records")
            ),
        }

        return json.dumps(
            report,
            indent=2,
            ensure_ascii=False,
            default=str
        )


tools = [
    DataQualityAnalysisTool()
]