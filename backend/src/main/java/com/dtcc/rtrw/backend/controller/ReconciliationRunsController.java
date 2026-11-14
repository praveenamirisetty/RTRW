package com.dtcc.rtrw.backend.controller;

import com.dtcc.rtrw.backend.dto.TableRowsDto;
import com.dtcc.rtrw.backend.service.MetadataService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/reconciliation/runs")
public class ReconciliationRunsController {
    private final MetadataService service;

    public ReconciliationRunsController(MetadataService service) {
        this.service = service;
    }

    @GetMapping
    public TableRowsDto list(@RequestParam(defaultValue = "100") int limit) {
        return service.rows("RECONCILIATION_RUN", limit);
    }
}
