from typing import Any

import pandas as pd


def standardize_text_columns(
    data: pd.DataFrame
) -> pd.DataFrame:
    """
    إزالة المسافات الزائدة وتوحيد كتابة النصوص.
    """
    cleaned_data = data.copy()

    text_columns = cleaned_data.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:
        cleaned_data[column] = (
            cleaned_data[column]
            .astype("string")
            .str.strip()
        )

    if "name" in cleaned_data.columns:
        cleaned_data["name"] = (
            cleaned_data["name"]
            .str.title()
        )

    if "city" in cleaned_data.columns:
        cleaned_data["city"] = (
            cleaned_data["city"]
            .str.title()
        )

    return cleaned_data


def clean_invalid_ages(
    data: pd.DataFrame
) -> pd.DataFrame:
    """
    استبدال الأعمار غير المنطقية بوسيط الأعمار الصحيحة.
    """
    cleaned_data = data.copy()

    if "age" not in cleaned_data.columns:
        return cleaned_data

    cleaned_data["age"] = pd.to_numeric(
        cleaned_data["age"],
        errors="coerce"
    )

    valid_age_mask = cleaned_data["age"].between(
        0,
        120,
        inclusive="both"
    )

    valid_ages = cleaned_data.loc[
        valid_age_mask,
        "age"
    ]

    if valid_ages.empty:
        return cleaned_data

    median_age = valid_ages.median()

    invalid_age_mask = (
        cleaned_data["age"].notna()
        & ~valid_age_mask
    )

    cleaned_data.loc[
        invalid_age_mask,
        "age"
    ] = median_age

    return cleaned_data


def clean_order_dates(
    data: pd.DataFrame
) -> pd.DataFrame:
    """
    تحويل التواريخ إلى DateTime.
    التاريخ غير الصحيح يتحول لقيمة مفقودة.
    """
    cleaned_data = data.copy()

    if "order_date" not in cleaned_data.columns:
        return cleaned_data

    cleaned_data["order_date"] = pd.to_datetime(
        cleaned_data["order_date"],
        errors="coerce"
    )

    return cleaned_data


def clean_missing_values(
    data: pd.DataFrame
) -> pd.DataFrame:
    """
    تعويض القيم الرقمية المفقودة بالوسيط،
    والنصوص المفقودة بكلمة Unknown.
    """
    cleaned_data = data.copy()

    numeric_columns = cleaned_data.select_dtypes(
        include="number"
    ).columns

    for column in numeric_columns:
        median_value = cleaned_data[column].median()

        if pd.notna(median_value):
            cleaned_data[column] = (
                cleaned_data[column]
                .fillna(median_value)
            )

    text_columns = cleaned_data.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:
        cleaned_data[column] = (
            cleaned_data[column]
            .fillna("Unknown")
        )

    return cleaned_data


def remove_duplicates(
    data: pd.DataFrame
) -> pd.DataFrame:
    """
    حذف الصفوف المكررة.
    """
    return (
        data
        .drop_duplicates()
        .reset_index(drop=True)
    )


def clean_dataset(
    data: pd.DataFrame
) -> pd.DataFrame:
    """
    تنفيذ خطوات التنظيف كاملة.
    """
    cleaned_data = data.copy()

    cleaned_data = standardize_text_columns(
        cleaned_data
    )

    cleaned_data = clean_invalid_ages(
        cleaned_data
    )

    cleaned_data = clean_order_dates(
        cleaned_data
    )

    cleaned_data = clean_missing_values(
        cleaned_data
    )

    cleaned_data = remove_duplicates(
        cleaned_data
    )

    return cleaned_data


def create_quality_report(
    original_data: pd.DataFrame,
    cleaned_data: pd.DataFrame
) -> dict[str, Any]:
    """
    مقارنة البيانات قبل وبعد التنظيف.
    """
    return {
        "original_rows": int(original_data.shape[0]),
        "cleaned_rows": int(cleaned_data.shape[0]),
        "removed_rows": int(
            original_data.shape[0]
            - cleaned_data.shape[0]
        ),
        "original_missing_values": int(
            original_data.isnull().sum().sum()
        ),
        "cleaned_missing_values": int(
            cleaned_data.isnull().sum().sum()
        ),
        "original_duplicates": int(
            original_data.duplicated().sum()
        ),
        "cleaned_duplicates": int(
            cleaned_data.duplicated().sum()
        ),
    }