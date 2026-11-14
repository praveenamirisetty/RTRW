
import json
from datetime import datetime, timezone

import pandas as pd

from config import RAW_DATA_DIR, REPORT_DIR


def analyze_order_warnings():

    file_path = RAW_DATA_DIR / "olist_orders_dataset.csv"

    df = pd.read_csv(file_path, low_memory=False)

    date_columns = [
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date"
    ]

    # Count missing dates by order status
    summary = (
        df.groupby("order_status", dropna=False)[date_columns]
        .agg(lambda column: int(column.isna().sum()))
        .reset_index()
    )

    summary_path = REPORT_DIR / "order_missing_dates_by_status.csv"
    summary.to_csv(summary_path, index=False)

    print("\nORDER MISSING DATES BY STATUS")
    print(summary.to_string(index=False))

    return {
        "total_orders": int(len(df)),
        "status_summary": summary.to_dict(orient="records")
    }


def analyze_product_warnings():

    file_path = RAW_DATA_DIR / "olist_products_dataset.csv"

    df = pd.read_csv(file_path, low_memory=False)

    descriptive_columns = [
        "product_category_name",
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty"
    ]

    dimension_columns = [
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm"
    ]

    descriptive_missing = df[descriptive_columns].isna().any(axis=1)
    dimensions_missing = df[dimension_columns].isna().any(axis=1)

    descriptive_only = descriptive_missing & ~dimensions_missing
    dimensions_only = dimensions_missing & ~descriptive_missing
    both_missing = descriptive_missing & dimensions_missing

    summary = {
        "total_products": int(len(df)),
        "products_with_missing_descriptive_fields": int(
            descriptive_missing.sum()
        ),
        "products_with_missing_dimensions": int(
            dimensions_missing.sum()
        ),
        "products_with_both_groups_missing": int(
            both_missing.sum()
        ),
        "products_with_only_descriptive_fields_missing": int(
            descriptive_only.sum()
        ),
        "products_with_only_dimensions_missing": int(
            dimensions_only.sum()
        )
    }

    affected = df[
        descriptive_missing | dimensions_missing
    ].copy()

    affected["missing_descriptive_fields"] = (
        descriptive_missing[affected.index]
    )

    affected["missing_dimensions"] = (
        dimensions_missing[affected.index]
    )

    affected_path = REPORT_DIR / "products_missing_metadata.csv"
    affected.to_csv(affected_path, index=False)

    print("\nPRODUCT MISSING METADATA SUMMARY")

    for key, value in summary.items():
        print(f"{key}: {value}")

    print("\nAffected product records saved to:")
    print(affected_path)

    return summary


def main():

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 75)
    print("RTRW DATA QUALITY WARNING ANALYSIS")
    print("=" * 75)

    order_results = analyze_order_warnings()
    product_results = analyze_product_warnings()

    report = {
        "report_name": "RTRW Warning Analysis",
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "orders": order_results,
        "products": product_results
    }

    output_path = REPORT_DIR / "warning_analysis.json"

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print("\nWarning analysis completed.")
    print("JSON report:", output_path)


if __name__ == "__main__":
    main()
