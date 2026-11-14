package com.dtcc.rtrw.backend.dto;

import java.time.Instant;
import java.util.Map;

public record ApiErrorDto(String error, String message, Instant timestamp, Map<String, String> fieldErrors) {
}
