package com.dtcc.rtrw.backend.controller;

import com.dtcc.rtrw.backend.dto.HealthDto;
import com.dtcc.rtrw.backend.dto.SnowflakeHealthDto;
import com.dtcc.rtrw.backend.service.HealthService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/health")
public class HealthController {
    private final HealthService service;

    public HealthController(HealthService service) {
        this.service = service;
    }

    @GetMapping
    public HealthDto health() {
        return new HealthDto("UP", "rtrw-backend");
    }

    @GetMapping("/snowflake")
    public SnowflakeHealthDto snowflake() {
        return service.check();
    }
}
