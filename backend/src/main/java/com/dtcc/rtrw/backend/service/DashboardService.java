package com.dtcc.rtrw.backend.service;

import com.dtcc.rtrw.backend.dto.DashboardOverviewDto;
import com.dtcc.rtrw.backend.enums.TableKey;
import com.dtcc.rtrw.backend.repository.SnowflakeReadRepository;
import com.dtcc.rtrw.backend.repository.TableCatalog;
import org.springframework.stereotype.Service;

import java.util.LinkedHashMap;
import java.util.Map;

@Service
public class DashboardService {
    private final SnowflakeReadRepository repository;
    private final TableCatalog catalog;

    public DashboardService(SnowflakeReadRepository repository, TableCatalog catalog) {
        this.repository = repository;
        this.catalog = catalog;
    }

    public DashboardOverviewDto overview() {
        Map<String, Long> counts = new LinkedHashMap<>();
        for (TableKey key : TableKey.values()) {
            try {
                counts.put(key.name(), repository.count(catalog.get(key)));
            } catch (Exception ex) {
                counts.put(key.name(), -1L);
            }
        }
        return new DashboardOverviewDto(counts);
    }
}
