package com.dtcc.rtrw.backend.repository;

import com.dtcc.rtrw.backend.enums.TableKey;
import com.dtcc.rtrw.backend.exception.ResourceNotFoundException;
import com.dtcc.rtrw.backend.model.TableDefinition;
import org.springframework.stereotype.Component;

import java.util.Collections;
import java.util.EnumMap;
import java.util.Map;

@Component
public class TableCatalog {
    private final Map<TableKey, TableDefinition> tables = new EnumMap<>(TableKey.class);

    public TableCatalog() {
        add(TableKey.RAW_ORDERS, "RAW", "RAW_ORDERS", "Raw order records");
        add(TableKey.RAW_PAYMENTS, "RAW", "RAW_PAYMENTS", "Raw payment records");
        add(TableKey.RAW_ORDER_ITEMS, "RAW", "RAW_ORDER_ITEMS", "Raw order item records");
        add(TableKey.RAW_CUSTOMERS, "RAW", "RAW_CUSTOMERS", "Raw customer records");
        add(TableKey.RAW_SELLERS, "RAW", "RAW_SELLERS", "Raw seller records");
        add(TableKey.RAW_PRODUCTS, "RAW", "RAW_PRODUCTS", "Raw product records");
        add(TableKey.RAW_REFUNDS, "RAW", "RAW_REFUNDS", "Refund records - verify this exact object name in Snowflake");
        add(TableKey.RECONCILIATION_RUN, "AUDIT", "RECONCILIATION_RUN", "Reconciliation run audit records");
        add(TableKey.RECONCILIATION_SNAPSHOT, "AUDIT", "RECONCILIATION_SNAPSHOT", "Reconciliation snapshots");
        add(TableKey.EXCEPTION_HISTORY, "AUDIT", "EXCEPTION_HISTORY", "Exception history");
        add(TableKey.DATA_QUALITY_RESULTS, "AUDIT", "DATA_QUALITY_RESULTS", "Data quality results");
        add(TableKey.S3_INGESTION_VALIDATION, "S3_EXT", "S3_INGESTION_VALIDATION", "S3 ingestion validation results");
    }

    private void add(TableKey key, String schema, String table, String description) {
        tables.put(key, new TableDefinition(key, schema, table, description));
    }

    public TableDefinition get(TableKey key) {
        TableDefinition d = tables.get(key);
        if (d == null) throw new ResourceNotFoundException("Unknown table key: " + key);
        return d;
    }

    public Map<TableKey, TableDefinition> all() {
        return Collections.unmodifiableMap(tables);
    }
}
