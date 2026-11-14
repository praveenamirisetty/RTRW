package com.dtcc.rtrw.backend.service;

import com.dtcc.rtrw.backend.dto.TableInfoDto;
import com.dtcc.rtrw.backend.dto.TableRowsDto;
import com.dtcc.rtrw.backend.enums.TableKey;
import com.dtcc.rtrw.backend.exception.ResourceNotFoundException;
import com.dtcc.rtrw.backend.model.TableDefinition;
import com.dtcc.rtrw.backend.repository.SnowflakeReadRepository;
import com.dtcc.rtrw.backend.repository.TableCatalog;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Locale;

@Service
public class MetadataService {
    private final TableCatalog catalog;
    private final SnowflakeReadRepository repository;

    public MetadataService(TableCatalog catalog, SnowflakeReadRepository repository) {
        this.catalog = catalog;
        this.repository = repository;
    }

    public List<TableInfoDto> tables() {
        return catalog.all().values().stream().map(t -> new TableInfoDto(t.key().name(), t.schema(), t.table(), t.description())).toList();
    }

    public TableRowsDto rows(String rawKey, int limit) {
        TableKey key;
        try {
            key = TableKey.valueOf(rawKey.toUpperCase(Locale.ROOT));
        } catch (IllegalArgumentException ex) {
            throw new ResourceNotFoundException("Unknown table key: " + rawKey);
        }
        TableDefinition d = catalog.get(key);
        int safe = Math.max(1, Math.min(limit, 500));
        return new TableRowsDto(key.name(), d.qualifiedName(), safe, repository.rows(d, safe));
    }
}
