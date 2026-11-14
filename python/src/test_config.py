
from config import (
    PROJECT_ROOT,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    REPORT_DIR,
    LOG_DIR,
    DATASET_CONFIG
)

print("RTRW CONFIGURATION TEST")
print("-" * 50)

print("Project root:", PROJECT_ROOT)
print("Raw data directory:", RAW_DATA_DIR)
print("Processed data directory:", PROCESSED_DATA_DIR)
print("Reports directory:", REPORT_DIR)
print("Logs directory:", LOG_DIR)

print("\nConfigured datasets:")

for name, config in DATASET_CONFIG.items():
    print(
        f"{name}: {config['file']} "
        f"({len(config['required_columns'])} columns)"
    )

print("\nConfiguration loaded successfully.")
