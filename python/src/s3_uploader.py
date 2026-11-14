
import boto3
from pathlib import Path
from datetime import datetime, timezone

# ==========================================
# PROJECT CONFIGURATION
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

BUCKET_NAME = "rtrw-devops"
AWS_REGION = "us-east-2"
AWS_PROFILE = "rtrw-dev"

# Local folders and their corresponding S3 folders
UPLOAD_FOLDERS = {
    PROJECT_ROOT / "datasets" / "processed": "processed",
    PROJECT_ROOT / "python" / "reports": "reports"
}


# ==========================================
# AWS CONNECTION
# ==========================================

def create_s3_client():
    session = boto3.Session(
        profile_name=AWS_PROFILE,
        region_name=AWS_REGION
    )

    return session.client("s3")


# ==========================================
# TEST S3 CONNECTION
# ==========================================

def test_s3_connection():
    try:
        session = boto3.Session(
            profile_name=AWS_PROFILE,
            region_name=AWS_REGION
        )

        s3 = session.client("s3")
        sts = session.client("sts")

        identity = sts.get_caller_identity()

        print("\nAWS connection successful")
        print("AWS account:", identity["Account"])

        test_key = "reports/boto3_connection_test.txt"

        test_content = (
            "RTRW Python Boto3 S3 connection successful\n"
            f"Tested at: {datetime.now(timezone.utc).isoformat()}\n"
        )

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=test_key,
            Body=test_content.encode("utf-8"),
            ContentType="text/plain"
        )

        print("Test file uploaded successfully")

        response = s3.head_object(
            Bucket=BUCKET_NAME,
            Key=test_key
        )

        print("S3 object verified")
        print("Object key:", test_key)
        print("Object size:", response["ContentLength"], "bytes")

        return True

    except Exception as error:
        print("\nS3 connection test failed:")
        print(type(error).__name__, error)
        raise


# ==========================================
# UPLOAD DATASETS AND REPORTS
# ==========================================

def upload_project_files():

    s3 = create_s3_client()

    total_uploaded = 0

    for local_folder, s3_folder in UPLOAD_FOLDERS.items():

        print(f"\nProcessing folder: {local_folder}")

        if not local_folder.exists():
            print("Folder does not exist. Skipping.")
            continue

        files = [
            file_path
            for file_path in local_folder.rglob("*")
            if file_path.is_file()
        ]

        if not files:
            print("No files found.")
            continue

        for file_path in files:

            relative_path = file_path.relative_to(local_folder)

            s3_key = (
                f"{s3_folder}/{relative_path.as_posix()}"
            )

            try:
                s3.upload_file(
                    str(file_path),
                    BUCKET_NAME,
                    s3_key
                )

                print(f"Uploaded successfully: {s3_key}")

                total_uploaded += 1

            except Exception as error:
                print(f"Upload failed: {file_path.name}")
                print(type(error).__name__, error)
                raise

    print("\n================================")
    print("S3 UPLOAD SUMMARY")
    print("================================")
    print("Total files uploaded:", total_uploaded)
    print("S3 bucket:", BUCKET_NAME)
    print("Upload completed successfully.")


# ==========================================
# MAIN EXECUTION
# ==========================================

if __name__ == "__main__":

    print("Starting RTRW S3 upload process...")

    test_s3_connection()

    upload_project_files()
