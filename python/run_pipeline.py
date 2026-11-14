
import json
import subprocess
import sys
from pathlib import Path


# ==================================================
# PROJECT PATHS
# ==================================================

PYTHON_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PYTHON_DIR.parent

SRC_DIR = PYTHON_DIR / "src"
TEST_DIR = PYTHON_DIR / "tests"
REPORT_DIR = PYTHON_DIR / "reports"

PYTHON_EXECUTABLE = sys.executable


# ==================================================
# RUN A PIPELINE STAGE
# ==================================================

def run_stage(command, description):

    print("\n" + "=" * 75)
    print(description)
    print("=" * 75)

    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT
    )

    if result.returncode != 0:
        print(f"\nFAILED: {description}")
        return False

    print(f"\nCOMPLETED: {description}")
    return True


# ==================================================
# VERIFY GENERATED REPORTS
# ==================================================

def verify_reports():

    print("\nVerifying generated reports...")

    required_files = [
        REPORT_DIR / "validation_report.csv",
        REPORT_DIR / "validation_report.json",
        REPORT_DIR / "data_quality_profile.json",
        REPORT_DIR / "data_quality_summary.csv",
        REPORT_DIR / "column_quality_report.csv",
        REPORT_DIR / "warning_analysis.json",
        REPORT_DIR / "order_missing_dates_by_status.csv",
        REPORT_DIR / "products_missing_metadata.csv"
    ]

    missing_files = [
        str(path)
        for path in required_files
        if not path.exists()
    ]

    if missing_files:
        print("Missing report files:")
        for path in missing_files:
            print(path)
        return False

    with open(
        REPORT_DIR / "validation_report.json",
        "r",
        encoding="utf-8"
    ) as file:
        report = json.load(file)

    print("\nValidation summary")
    print("Total checks:", report["total_checks"])
    print("Passed:", report["passed"])
    print("Failed:", report["failed"])
    print("Warnings:", report["warnings"])

    if report["failed"] > 0:
        print("\nValidation failures detected.")
        return False

    print("\nAll required reports exist.")
    return True


# ==================================================
# MAIN PIPELINE
# ==================================================

def main():

    print("\n" + "=" * 75)
    print("RTRW AUTOMATED DATA QUALITY PIPELINE")
    print("=" * 75)

    # Stage 1: Data profiling
    if not run_stage(
        [
            PYTHON_EXECUTABLE,
            str(SRC_DIR / "profile_data.py")
        ],
        "STAGE 1: DATA PROFILING"
    ):
        sys.exit(1)

    # Stage 2: Warning analysis
    if not run_stage(
        [
            PYTHON_EXECUTABLE,
            str(SRC_DIR / "analyze_warnings.py")
        ],
        "STAGE 2: WARNING ANALYSIS"
    ):
        sys.exit(1)

    # Stage 3: Dataset validation
    if not run_stage(
        [
            PYTHON_EXECUTABLE,
            str(SRC_DIR / "validator.py")
        ],
        "STAGE 3: DATASET VALIDATION"
    ):
        sys.exit(1)

    # Stage 4: Verify reports
    if not verify_reports():
        print("\nPipeline stopped during report verification.")
        sys.exit(1)

    # Stage 5: Automated tests
    if not run_stage(
        [
            PYTHON_EXECUTABLE,
            "-m",
            "pytest",
            str(TEST_DIR),
            "-v"
        ],
        "STAGE 5: AUTOMATED TESTS"
    ):
        sys.exit(1)

    # Final result
    print("\n" + "=" * 75)
    print("RTRW DATA QUALITY PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 75)

    print("Data profiling       : COMPLETED")
    print("Warning analysis     : COMPLETED")
    print("Dataset validation   : COMPLETED")
    print("Report verification  : PASSED")
    print("Automated tests      : PASSED")

    print("\nOutput directories:")
    print("datasets/processed/")
    print("python/reports/")
    print("python/logs/")


if __name__ == "__main__":
    main()
