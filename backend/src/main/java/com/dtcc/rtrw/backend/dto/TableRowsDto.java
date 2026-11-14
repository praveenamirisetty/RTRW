package com.dtcc.rtrw.backend.dto;

import java.util.List;
import java.util.Map;

public record TableRowsDto(String key, String qualifiedTable, int limit, List<Map<String, Object>> rows) {
}
