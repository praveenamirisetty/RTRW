# AWS S3 Integration – RTRW

## 1. Objective
Integrate Amazon S3 with Snowflake to provide external storage for raw datasets, processed datasets and data-quality reports.

## 2. AWS S3 Configuration
- Bucket: `rtrw-devops`
- Region: `us-east-2`
- Encryption: SSE-S3
- Block Public Access: Enabled
- Object Ownership: ACLs disabled

### Bucket folders
- `raw/` – Original source CSV files
- `processed/` – Validated and processed CSV files
- `reports/` – Data-quality and validation reports
- `archive/` – Reserved for archived files

## 3. IAM Configuration
- IAM policy: `RTRW_Snowflake_S3_Read_Policy`
- IAM role: `RTRW_Snowflake_S3_Role`
- Permissions configured for Snowflake to access the required S3 bucket locations.

## 4. Snowflake Integration
- Database: `RTRW_DB`
- Schema: `S3_EXT`
- Storage integration: `RTRW_S3_INT`
- External stage: `RTRW_S3_STAGE`
- CSV file format: `RTRW_S3_CSV_FORMAT`

## 5. Data Ingestion
Seven datasets were loaded from the S3 processed folder into isolated Snowflake test tables.

| Dataset | Rows loaded |
|---|---:|
| Orders | 99,441 |
| Payments | 103,886 |
| Order items | 112,650 |
| Customers | 99,441 |
| Sellers | 3,095 |
| Products | 32,951 |
| Refunds | 5,387 |
| **Total** | **456,851** |

## 6. Validation Results
S3 test-table record counts were compared against the existing Snowflake RAW tables.

- Total datasets validated: 7
- Passed: 7
- Failed: 0
- S3 records: 456,851
- RAW records: 456,851

All seven dataset row counts matched.

## 7. Audit
Created the Snowflake table:

`RTRW_DB.S3_EXT.S3_INGESTION_VALIDATION`

This table records dataset names, S3 row counts, RAW row counts, validation status and validation timestamps.

## 8. Security
- S3 public access is blocked.
- Server-side encryption is enabled.
- Snowflake access uses an IAM role and storage integration.
- Existing Snowflake RAW and downstream project tables were preserved.

## 9. Outcome
Successfully established and tested connectivity between Amazon S3 and Snowflake. Verified ingestion of all seven datasets and recorded the validation results in Snowflake.

**Phase Status: Completed**
