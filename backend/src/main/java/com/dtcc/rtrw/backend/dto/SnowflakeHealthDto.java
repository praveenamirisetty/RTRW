package com.dtcc.rtrw.backend.dto;

public record SnowflakeHealthDto(String status, String database, String schema, String warehouse, String message) {
}
