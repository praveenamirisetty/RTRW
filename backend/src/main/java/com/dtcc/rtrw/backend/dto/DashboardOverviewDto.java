package com.dtcc.rtrw.backend.dto;

import java.util.Map;

public record DashboardOverviewDto(Map<String, Long> tableCounts) {
}
