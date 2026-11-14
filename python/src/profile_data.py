
import json
from datetime import datetime, timezone

import pandas as pd

from config import (
    RAW_DATA_DIR,
    REPORT_DIR,
    DATASET_CONFIG,
    STRING_COLUMNS
)


# ==================================================
# 1. PROFILE ONE DATASET
# ==================================================

def profile_dataset(dataset_name, config):

    file_path = RAW_DATA_DIR / config["file"]

    print(f"\nProfiling: {config['file']}")

    if not file_path.exists():
        print("File not found")
        return None

    dtype_mapping = {
        column: "string"
        for column in STRING_COLUMNS
    }

    df = pd.read_csv(
        file_path,
        low_memory=False,
        dtype=dtype_mapping
    )

    column_profiles = []

    for column in df.columns:

        series = df[column]

        profile = {
            "column_name": column,
            "data_type": str(series.dtype),
            "total_records": int(len(series)),
            "missing_values": int(series.isna().sum()),
            "missing_percentage": round(
                float(series.isna().mean() * 100), 2
            ),
            "unique_values": int(series.nunique(dropna=True))
        }

        if pd.api.types.is_numeric_dtype(series):

            profile["minimum"] = (
                None if series.dropna().empty
                else float(series.min())
            )

            profile["maximum"] = (
                None if series.dropna().empty
                else float(series.max())
            )

            profile["average"] = (
                None if series.dropna().empty
                else float(series.mean())
            )

        column_profiles.append(profile)

    return {
        "dataset_name": dataset_name,
        "file_name": config["file"],
        "total_records": int(len(df)),
        "total_columns": int(len(df.columns)),
        "duplicate_rows": int(df.duplicated().sum()),
        "column_profiles": column_profiles
    }


# ==================================================
# 2. GENERATE DATA QUALITY PROFILE
# ==================================================

def main():

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    dataset_profiles = []

    for dataset_name, config in DATASET_CONFIG.items():

        try:

            profile = profile_dataset(
                dataset_name,
                config
            )

            if profile is not None:
                dataset_profiles.append(profile)

        except Exception as error:

            print(
                f"Error profiling {dataset_name}: {error}"
            )

    # JSON report
    json_output = {
        "report_name": "RTRW Data Quality Profile",
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "datasets_profiled": len(dataset_profiles),
        "datasets": dataset_profiles
    }

    json_path = (
        REPORT_DIR / "data_quality_profile.json"
    )

    with open(
        json_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            json_output,
            file,
            indent=4
        )

    # Dataset-level CSV summary
    summary_rows = []

    for profile in dataset_profiles:

        summary_rows.append({
            "dataset_name": profile["dataset_name"],
            "file_name": profile["file_name"],
            "total_records": profile["total_records"],
            "total_columns": profile["total_columns"],
            "duplicate_rows": profile["duplicate_rows"]
        })

    summary_df = pd.DataFrame(summary_rows)

    csv_path = (
        REPORT_DIR / "data_quality_summary.csv"
    )

    summary_df.to_csv(
        csv_path,
        index=False
    )

    # Column-level CSV report
    column_rows = []

    for profile in dataset_profiles:

        for column in profile["column_profiles"]:

            column_rows.append({
                "dataset_name": profile["dataset_name"],
                **column
            })

    column_df = pd.DataFrame(column_rows)

    column_path = (
        REPORT_DIR / "column_quality_report.csv"
    )

    column_df.to_csv(
        column_path,
        index=False
    )

    print("\n" + "=" * 70)
    print("RTRW DATA PROFILING COMPLETED")
    print("=" * 70)

    print(summary_df.to_string(index=False))

    print("\nGenerated reports:")
    print(json_path)
    print(csv_path)
    print(column_path)


if __name__ == "__main__":
    main()
