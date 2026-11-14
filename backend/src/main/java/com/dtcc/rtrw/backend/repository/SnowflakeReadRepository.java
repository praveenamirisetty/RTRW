package com.dtcc.rtrw.backend.repository;

import com.dtcc.rtrw.backend.model.TableDefinition;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Map;

@Repository
public class SnowflakeReadRepository {
    private final JdbcTemplate jdbc;

    public SnowflakeReadRepository(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    public Map<String, Object> connectionInfo() {
        return jdbc.queryForMap("SELECT CURRENT_DATABASE() AS DATABASE_NAME, CURRENT_SCHEMA() AS SCHEMA_NAME, CURRENT_WAREHOUSE() AS WAREHOUSE_NAME");
    }

    public long count(TableDefinition table) {
        Long n = jdbc.queryForObject("SELECT COUNT(*) FROM " + table.qualifiedName(), Long.class);
        return n == null ? 0 : n;
    }

    public List<Map<String, Object>> rows(TableDefinition table, int limit) {
        int safe = Math.max(1, Math.min(limit, 500));
        return jdbc.queryForList("SELECT * FROM " + table.qualifiedName() + " LIMIT " + safe);
    }
}
