
from pathlib import Path
import pandas as pd

# Locate the RTRW root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Existing source dataset location
RAW_DATA_DIR = PROJECT_ROOT / "datasets" / "raw"

DATASET_FILES = [
    "olist_orders_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_sellers_dataset.csv",
    "olist_products_dataset.csv",
    "refunds_dataset.csv"
]


def inspect_dataset(filename):
    file_path = RAW_DATA_DIR / filename

    print("\n" + "=" * 80)
    print(f"DATASET: {filename}")
    print("=" * 80)

    if not file_path.exists():
        print("ERROR: File not found")
        return

    try:
        # Read a small sample first
        df = pd.read_csv(
            file_path,
            nrows=5,
            low_memory=False
        )

        print("\nCOLUMN NAMES:")
        print(df.columns.tolist())

        print("\nSAMPLE RECORDS:")
        print(df.head(3).to_string(index=False))

        # Read column metadata
        full_df = pd.read_csv(
            file_path,
            nrows=0
        )

        print("\nCOLUMN COUNT:")
        print(len(full_df.columns))

        print("\nFILE SIZE:")
        print(f"{file_path.stat().st_size:,} bytes")

    except Exception as error:
        print(f"ERROR: {error}")


def main():
    print("RTRW DATASET INSPECTION")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Source directory: {RAW_DATA_DIR}")

    for filename in DATASET_FILES:
        inspect_dataset(filename)

    print("\nDATASET INSPECTION COMPLETED")


if __name__ == "__main__":
    main()
