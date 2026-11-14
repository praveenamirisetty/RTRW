CREATE SCHEMA IF NOT EXISTS RTRW_DB.RAW
COMMENT = 'Original source datasets';

CREATE SCHEMA IF NOT EXISTS RTRW_DB.STAGING
COMMENT = 'Cleaned and standardized datasets';

CREATE SCHEMA IF NOT EXISTS RTRW_DB.CORE
COMMENT = 'Financial data warehouse and reconciliation model';

CREATE SCHEMA IF NOT EXISTS RTRW_DB.AUDIT
COMMENT = 'Data quality, reconciliation and audit history';

CREATE SCHEMA IF NOT EXISTS RTRW_DB.ANALYTICS
COMMENT = 'Business intelligence and reporting views';

SHOW SCHEMAS IN DATABASE RTRW_DB;

USE SCHEMA RTRW_DB.RAW;