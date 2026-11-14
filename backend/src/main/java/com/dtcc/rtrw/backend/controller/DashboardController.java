
package com.dtcc.rtrw.backend.controller;

import com.dtcc.rtrw.backend.dto.DashboardOverviewDto;
import com.dtcc.rtrw.backend.dto.TableRowsDto;
import com.dtcc.rtrw.backend.service.DashboardService;
import com.dtcc.rtrw.backend.service.MetadataService;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/dashboard")
public class DashboardController {

    private final DashboardService service;
    private final MetadataService metadataService;

    public DashboardController(
            DashboardService service,
            MetadataService metadataService) {
        this.service = service;
        this.metadataService = metadataService;
    }

    @GetMapping("/overview")
    public DashboardOverviewDto overview() {
        return service.overview();
    }

    @GetMapping("/data-quality")
    public TableRowsDto dataQuality(
            @RequestParam(defaultValue = "100") int limit) {

        return metadataService.rows("DATA_QUALITY_RESULTS", limit);
    }
}
