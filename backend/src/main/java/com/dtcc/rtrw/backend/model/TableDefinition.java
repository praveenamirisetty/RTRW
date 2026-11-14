package com.dtcc.rtrw.backend.model;

import com.dtcc.rtrw.backend.enums.TableKey;

public record TableDefinition(TableKey key, String schema, String table, String description) {
    public String qualifiedName() {
        return "RTRW_DB." + schema + "." + table;
    }
}
