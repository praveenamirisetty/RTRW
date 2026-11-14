# RTRW Backend

Spring Boot REST API for the Returns-to-Refund Financial Reconciliation Warehouse.

## Stack
- Java 21
- Spring Boot 3.5.16
- Spring JDBC / JdbcTemplate
- Snowflake JDBC 3.28.0
- Springdoc OpenAPI / Swagger UI

## Configure Snowflake
Edit `src/main/resources/application.properties` and replace:
- `YOUR_ACCOUNT_IDENTIFIER` with your Snowflake account identifier (not a full URL)
- `YOUR_SNOWFLAKE_USERNAME` with your username
- `YOUR_SNOWFLAKE_PASSWORD` with your password

The JDBC URL defaults to warehouse `RTRW_WH`, database `RTRW_DB`, schema `ANALYTICS`. Do not commit the properties file; it is in `.gitignore`.

## IntelliJ setup
1. Extract the ZIP.
2. IntelliJ IDEA > Open > select the extracted `RTRW_Backend_IntelliJ` folder (the folder containing `pom.xml`).
3. Select JDK 21 as Project SDK.
4. Allow IntelliJ to import/reload the Maven project and download dependencies.
5. Edit `application.properties` with your own Snowflake credentials.
6. Run `BackendApplication` or use the Maven tool window > Lifecycle > `spring-boot:run`.

## PowerShell
From the folder containing `pom.xml`:
```powershell
mvn clean
mvn spring-boot:run
```
The Spring Boot Maven plugin is configured with `fork=true` and the Java `--add-opens` option required by the Arrow component bundled with this Snowflake JDBC driver.

## Endpoints
- `GET http://localhost:8080/api/health`
- `GET http://localhost:8080/api/health/snowflake`
- `GET http://localhost:8080/api/dashboard/overview`
- `GET http://localhost:8080/api/metadata/tables`
- `GET http://localhost:8080/api/metadata/tables/RAW_ORDERS?limit=100`
- `GET http://localhost:8080/api/refunds?limit=100`
- `GET http://localhost:8080/api/exceptions?limit=100`
- `GET http://localhost:8080/api/reconciliation/runs?limit=100`
- `GET http://localhost:8080/api/reconciliation/snapshots?limit=100`
- `GET http://localhost:8080/api/ingestion/validation?limit=100`
- Swagger: `http://localhost:8080/swagger-ui/index.html`

## Important assumptions to verify
The table catalog uses the object names discussed for this project: RAW tables (`RAW_ORDERS`, `RAW_PAYMENTS`, `RAW_ORDER_ITEMS`, `RAW_CUSTOMERS`, `RAW_SELLERS`, `RAW_PRODUCTS`, `RAW_REFUNDS`), AUDIT tables (`RECONCILIATION_RUN`, `RECONCILIATION_SNAPSHOT`, `EXCEPTION_HISTORY`, `DATA_QUALITY_RESULTS`) and `S3_EXT.S3_INGESTION_VALIDATION`. Confirm the exact names in Snowflake before relying on those endpoints. In particular, confirm the refund table name and audit table names.

This starter backend is read-only. Dashboard overview returns row counts by catalog table; `-1` means a table count could not be read. Named list endpoints return raw rows, because the exact column definitions have not been verified here. No writes or reconciliation calculations are performed by this API.
