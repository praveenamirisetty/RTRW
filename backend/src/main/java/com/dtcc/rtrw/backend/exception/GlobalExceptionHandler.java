package com.dtcc.rtrw.backend.exception;

import com.dtcc.rtrw.backend.dto.ApiErrorDto;
import org.springframework.dao.DataAccessException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.time.Instant;
import java.util.Map;

@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ApiErrorDto> notFound(ResourceNotFoundException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(new ApiErrorDto("NOT_FOUND", ex.getMessage(), Instant.now(), Map.of()));
    }

    @ExceptionHandler(DataAccessException.class)
    public ResponseEntity<ApiErrorDto> database(DataAccessException ex) {
        return ResponseEntity.status(500).body(new ApiErrorDto("DATABASE_ERROR", "Snowflake query failed. Check the backend console for the underlying JDBC/SQL error, table existence and SELECT grants.", Instant.now(), Map.of()));
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ApiErrorDto> other(Exception ex) {
        return ResponseEntity.status(500).body(new ApiErrorDto("INTERNAL_ERROR", "An unexpected backend error occurred.", Instant.now(), Map.of()));
    }
}
