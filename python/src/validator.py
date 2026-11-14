
import json
import logging
from datetime import datetime, timezone

import pandas as pd

try:
    from .config import (
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        REPORT_DIR,
        LOG_DIR,
        DATASET_CONFIG,
        STRING_COLUMNS
    )
except ImportError:
    from config import (
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        REPORT_DIR,
        LOG_DIR,
        DATASET_CONFIG,
        STRING_COLUMNS
    )

# ==================================================
# 1. LOGGING CONFIGURATION
# ==================================================

logging.basicConfig(
    filename=LOG_DIR / "validation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


# ==================================================
# 2. VALIDATION RESULT STORAGE
# ==================================================

validation_results = []

loaded_datasets = {}


def add_result(
    dataset,
    check,
    status,
    details,
    count=0
):
    validation_results.append({
        "dataset": dataset,
        "check": check,
        "status": status,
        "count": int(count),
        "details": str(details)
    })

    if status == "FAILED":
        logging.error("%s - %s - %s", dataset, check, details)

    elif status == "WARNING":
        logging.warning("%s - %s - %s", dataset, check, details)

    else:
        logging.info("%s - %s - %s", dataset, check, details)


# ==================================================
# 3. READ SOURCE CSV
# ==================================================

def read_dataset(dataset_name, config):

    file_path = RAW_DATA_DIR / config["file"]

    if not file_path.exists():

        add_result(
            dataset_name,
            "File existence",
            "FAILED",
            f"File not found: {file_path}"
        )

        return None

    try:

        dtype_mapping = {
            column: "string"
            for column in STRING_COLUMNS
        }

        df = pd.read_csv(
            file_path,
            low_memory=False,
            dtype=dtype_mapping
        )

        if df.empty:

            add_result(
                dataset_name,
                "File content",
                "FAILED",
                "CSV file contains no records"
            )

            return None

        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
        )

        add_result(
            dataset_name,
            "File existence",
            "PASSED",
            f"Successfully loaded {config['file']}",
            len(df)
        )

        return df

    except Exception as error:

        add_result(
            dataset_name,
            "CSV reading",
            "FAILED",
            str(error)
        )

        logging.exception(
            "Unable to read %s",
            config["file"]
        )

        return None


# ==================================================
# 4. REQUIRED COLUMN VALIDATION
# ==================================================

def validate_columns(dataset_name, df, required_columns):

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        add_result(
            dataset_name,
            "Required columns",
            "FAILED",
            f"Missing columns: {missing_columns}",
            len(missing_columns)
        )

        return False

    add_result(
        dataset_name,
        "Required columns",
        "PASSED",
        "All required columns are present"
    )

    return True


# ==================================================
# 5. REQUIRED NON-NULL VALIDATION
# ==================================================

def validate_required_values(
    dataset_name,
    df,
    required_non_null
):

    for column in required_non_null:

        if column not in df.columns:
            continue

        missing_count = int(
            df[column].isna().sum()
        )

        if missing_count > 0:

            add_result(
                dataset_name,
                f"Required values: {column}",
                "FAILED",
                f"{missing_count} null values found",
                missing_count
            )

        else:

            add_result(
                dataset_name,
                f"Required values: {column}",
                "PASSED",
                "No null values found"
            )


# ==================================================
# 6. MISSING VALUE ANALYSIS
# ==================================================

def validate_missing_values(dataset_name, df):

    missing_columns = df.columns[
        df.isna().any()
    ]

    if len(missing_columns) == 0:

        add_result(
            dataset_name,
            "Missing value analysis",
            "PASSED",
            "No missing values found"
        )

        return

    for column in missing_columns:

        missing_count = int(
            df[column].isna().sum()
        )

        add_result(
            dataset_name,
            f"Missing values: {column}",
            "WARNING",
            f"{missing_count} missing values",
            missing_count
        )


# ==================================================
# 7. DUPLICATE KEY VALIDATION
# ==================================================

def validate_duplicates(dataset_name, df, unique_key):

    duplicate_count = int(
        df.duplicated(
            subset=unique_key,
            keep=False
        ).sum()
    )

    if duplicate_count > 0:

        add_result(
            dataset_name,
            "Duplicate key validation",
            "FAILED",
            f"Duplicate records found for {unique_key}",
            duplicate_count
        )

    else:

        add_result(
            dataset_name,
            "Duplicate key validation",
            "PASSED",
            f"No duplicate keys found for {unique_key}"
        )


# ==================================================
# 8. DATE VALIDATION
# ==================================================

def validate_dates(dataset_name, df, date_columns):

    for column in date_columns:

        if column not in df.columns:
            continue

        original = df[column]

        parsed = pd.to_datetime(
            original,
            errors="coerce"
        )

        invalid_mask = (
            original.notna()
            & parsed.isna()
        )

        invalid_count = int(
            invalid_mask.sum()
        )

        if invalid_count > 0:

            add_result(
                dataset_name,
                f"Date validation: {column}",
                "FAILED",
                f"Invalid dates found in {column}",
                invalid_count
            )

        else:

            add_result(
                dataset_name,
                f"Date validation: {column}",
                "PASSED",
                "Non-null date values are valid"
            )

        df[column] = parsed


# ==================================================
# 9. NUMERIC VALIDATION
# ==================================================

def validate_numeric(dataset_name, df, numeric_columns):

    for column in numeric_columns:

        if column not in df.columns:
            continue

        original = df[column]

        parsed = pd.to_numeric(
            original,
            errors="coerce"
        )

        invalid_mask = (
            original.notna()
            & parsed.isna()
        )

        invalid_count = int(
            invalid_mask.sum()
        )

        if invalid_count > 0:

            add_result(
                dataset_name,
                f"Numeric validation: {column}",
                "FAILED",
                f"Invalid numeric values in {column}",
                invalid_count
            )

        else:

            add_result(
                dataset_name,
                f"Numeric validation: {column}",
                "PASSED",
                "Numeric values are valid"
            )

        df[column] = parsed


# ==================================================
# 10. FINANCIAL AMOUNT VALIDATION
# ==================================================

def validate_amounts(dataset_name, df, amount_columns):

    for column in amount_columns:

        if column not in df.columns:
            continue

        negative_count = int(
            (df[column].dropna() < 0).sum()
        )

        if negative_count > 0:

            add_result(
                dataset_name,
                f"Financial amount: {column}",
                "WARNING",
                f"{negative_count} negative values found",
                negative_count
            )

        else:

            add_result(
                dataset_name,
                f"Financial amount: {column}",
                "PASSED",
                "No negative values found"
            )


# ==================================================
# 11. SYNTHETIC REFUND VALIDATION
# ==================================================

def validate_refund_origin(df):

    if "data_origin" not in df.columns:
        return

    origin_values = (
        df["data_origin"]
        .dropna()
        .astype(str)
        .str.strip()
        .str.upper()
    )

    invalid_count = int(
        (~origin_values.eq("SYNTHETIC")).sum()
    )

    if invalid_count > 0:

        add_result(
            "refunds",
            "Synthetic refund origin",
            "FAILED",
            "Unexpected DATA_ORIGIN values found",
            invalid_count
        )

    else:

        add_result(
            "refunds",
            "Synthetic refund origin",
            "PASSED",
            "All non-null refund origin values are SYNTHETIC"
        )


# ==================================================
# 12. VALIDATE ONE DATASET
# ==================================================

def validate_dataset(dataset_name, config):

    print(f"\nValidating dataset: {dataset_name}")

    df = read_dataset(
        dataset_name,
        config
    )

    if df is None:
        return None

    columns_valid = validate_columns(
        dataset_name,
        df,
        config["required_columns"]
    )

    if not columns_valid:
        return None

    validate_required_values(
        dataset_name,
        df,
        config["required_non_null"]
    )

    validate_missing_values(
        dataset_name,
        df
    )

    validate_duplicates(
        dataset_name,
        df,
        config["unique_key"]
    )

    validate_dates(
        dataset_name,
        df,
        config["date_columns"]
    )

    validate_numeric(
        dataset_name,
        df,
        config["numeric_columns"]
    )

    validate_amounts(
        dataset_name,
        df,
        config["amount_columns"]
    )

    if dataset_name == "refunds":
        validate_refund_origin(df)

    loaded_datasets[dataset_name] = df

    return df


# ==================================================
# 13. REFERENTIAL INTEGRITY VALIDATION
# ==================================================

def validate_reference(
    source_name,
    source_df,
    source_column,
    target_name,
    target_df,
    target_column
):

    if source_df is None or target_df is None:
        return

    source_values = source_df[source_column].dropna()
    target_values = set(
        target_df[target_column].dropna()
    )

    unmatched_count = int(
        (~source_values.isin(target_values)).sum()
    )

    if unmatched_count > 0:

        add_result(
            source_name,
            f"Reference to {target_name}",
            "FAILED",
            f"{unmatched_count} records reference unknown {target_name}",
            unmatched_count
        )

    else:

        add_result(
            source_name,
            f"Reference to {target_name}",
            "PASSED",
            f"All references to {target_name} are valid"
        )


def validate_references(datasets):

    print("\nValidating cross-dataset relationships...")

    # Orders -> Customers
    validate_reference(
        "orders",
        datasets.get("orders"),
        "customer_id",
        "customers",
        datasets.get("customers"),
        "customer_id"
    )

    # Payments -> Orders
    validate_reference(
        "payments",
        datasets.get("payments"),
        "order_id",
        "orders",
        datasets.get("orders"),
        "order_id"
    )

    # Order items -> Orders
    validate_reference(
        "order_items",
        datasets.get("order_items"),
        "order_id",
        "orders",
        datasets.get("orders"),
        "order_id"
    )

    # Order items -> Products
    validate_reference(
        "order_items",
        datasets.get("order_items"),
        "product_id",
        "products",
        datasets.get("products"),
        "product_id"
    )

    # Order items -> Sellers
    validate_reference(
        "order_items",
        datasets.get("order_items"),
        "seller_id",
        "sellers",
        datasets.get("sellers"),
        "seller_id"
    )

    # Refunds -> Orders
    validate_reference(
        "refunds",
        datasets.get("refunds"),
        "order_id",
        "orders",
        datasets.get("orders"),
        "order_id"
    )

    # Refunds -> Customers
    validate_reference(
        "refunds",
        datasets.get("refunds"),
        "customer_id",
        "customers",
        datasets.get("customers"),
        "customer_id"
    )


# ==================================================
# 14. SAVE VALIDATED DATASETS
# ==================================================

def save_validated_datasets(datasets):

    print("\nPreparing validated datasets...")

    for dataset_name, df in datasets.items():

        if df is None:
            continue

        # Check whether this dataset has any failed checks.
        failed_checks = [
            result
            for result in validation_results
            if result["dataset"] == dataset_name
            and result["status"] == "FAILED"
        ]

        if failed_checks:

            add_result(
                dataset_name,
                "Processed output",
                "FAILED",
                "Output not generated because validation failures exist"
            )

            continue

        output_file = (
            PROCESSED_DATA_DIR
            / DATASET_CONFIG[dataset_name]["file"]
        )

        df.to_csv(
            output_file,
            index=False
        )

        add_result(
            dataset_name,
            "Processed output",
            "PASSED",
            f"Validated file saved: {output_file.name}",
            len(df)
        )

        print(f"Saved: {output_file}")


# ==================================================
# 15. GENERATE REPORTS
# ==================================================

def generate_reports():

    report_df = pd.DataFrame(
        validation_results
    )

    csv_report = REPORT_DIR / "validation_report.csv"
    json_report = REPORT_DIR / "validation_report.json"

    report_df.to_csv(
        csv_report,
        index=False
    )

    report_data = {
        "pipeline": "RTRW Python Pandas Validation Pipeline",

        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),

        "total_checks": len(report_df),

        "passed": int(
            (report_df["status"] == "PASSED").sum()
        ),

        "failed": int(
            (report_df["status"] == "FAILED").sum()
        ),

        "warnings": int(
            (report_df["status"] == "WARNING").sum()
        ),

        "results": validation_results
    }

    with open(
        json_report,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report_data,
            file,
            indent=4
        )

    print("\nVALIDATION REPORT")
    print("=" * 80)

    print(
        report_df.to_string(index=False)
    )

    print("\nReport files generated:")
    print(csv_report)
    print(json_report)

    return report_data


# ==================================================
# 16. MAIN PIPELINE
# ==================================================

def main():

    print("\n" + "=" * 80)
    print("RTRW DATA VALIDATION PIPELINE")
    print("=" * 80)

    datasets = {}

    # Validate all configured datasets
    for dataset_name, config in DATASET_CONFIG.items():

        datasets[dataset_name] = validate_dataset(
            dataset_name,
            config
        )

    # Validate relationships across datasets
    validate_references(datasets)

    # Save only datasets with no failed checks
    save_validated_datasets(datasets)

    # Generate CSV and JSON reports
    report = generate_reports()

    print("\n" + "=" * 80)

    if report["failed"] > 0:

        print("PIPELINE STATUS: FAILED")
        print(f"Failed checks: {report['failed']}")

    else:

        print("PIPELINE STATUS: NO FAILED CHECKS")
        print("Review warnings before approving the data.")

    print("=" * 80)


if __name__ == "__main__":
    main()
