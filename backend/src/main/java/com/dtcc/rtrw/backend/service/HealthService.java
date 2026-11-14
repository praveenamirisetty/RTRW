package com.dtcc.rtrw.backend.service;

import com.dtcc.rtrw.backend.dto.SnowflakeHealthDto;
import com.dtcc.rtrw.backend.repository.SnowflakeReadRepository;
import org.springframework.stereotype.Service;

import java.util.Map;

@Service
public class HealthService {
    private final SnowflakeReadRepository repository;

    public HealthService(SnowflakeReadRepository repository) {
        this.repository = repository;
    }

    public SnowflakeHealthDto check() {
        Map<String, Object> m = repository.connectionInfo();
        return new SnowflakeHealthDto("UP", String.valueOf(m.get("DATABASE_NAME")), String.valueOf(m.get("SCHEMA_NAME")), String.valueOf(m.get("WAREHOUSE_NAME")), "Snowflake query succeeded");
    }
}
