package com.dtcc.rtrw.backend.controller;

import com.dtcc.rtrw.backend.dto.TableInfoDto;
import com.dtcc.rtrw.backend.dto.TableRowsDto;
import com.dtcc.rtrw.backend.service.MetadataService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/metadata")
public class MetadataController {
    private final MetadataService service;

    public MetadataController(MetadataService service) {
        this.service = service;
    }

    @GetMapping("/tables")
    public List<TableInfoDto> tables() {
        return service.tables();
    }

    @GetMapping("/tables/{key}")
    public TableRowsDto rows(@PathVariable String key, @RequestParam(defaultValue = "100") int limit) {
        return service.rows(key, limit);
    }
}
