import { useState, useMemo, useEffect } from 'react';
import type { Player, TableColumn, TableSort, ColumnFilters, ColumnVisibility } from '../../types/player';
import { getTeamColor, getTeamLogoUrl } from '../../utils/teamColors';
import './DataTable.css';

interface DataTableProps {
  players: Player[];
}

const DataTable = ({ players }: DataTableProps) => {
  // Table state
  const [searchTerm, setSearchTerm] = useState('');
  const [sortConfig, setSortConfig] = useState<TableSort>({ key: undefined, column: null, direction: 'asc' });
  const [currentPage, setCurrentPage] = useState(1);
  const [showColumnMenu, setShowColumnMenu] = useState(false);
  const [activeFilterColumn, setActiveFilterColumn] = useState<string | null>(null);

  const [visibleColumns, setVisibleColumns] = useState<ColumnVisibility>({
    player_name: true,
    position: true,
    team_abbr: true,
    salary: true,
    dk_projection: true,
    std_dev: true,
    ceiling: true,
    boom_pct: true,
    bust_pct: true,
    ownership_pct: true,
    optimal_pct: true,
    leverage: true
  });

  // Column filters
  const [columnFilters, setColumnFilters] = useState<ColumnFilters>({
    searchTerm: '',
    selectedTeams: [],
    selectedPositions: [],
    position: [],
    team_abbr: [],
    salaryMin: 0,
    salaryMax: 100000,
    ownershipMin: 0,
    ownershipMax: 100,
    leverageMin: -100,
    leverageMax: 100,
    salary: { min: '', max: '' },
    dk_projection: { min: '', max: '' },
    std_dev: { min: '', max: '' },
    ceiling: { min: '', max: '' },
    boom_pct: { min: '', max: '' },
    bust_pct: { min: '', max: '' },
    ownership_pct: { min: '', max: '' },
    optimal_pct: { min: '', max: '' },
    leverage: { min: '', max: '' }
  });

  const itemsPerPage = 25;

  // Column definitions
  const columns: TableColumn[] = [
    { key: 'player_name', label: 'Player', sortable: true, locked: true, type: 'text' },
    { key: 'team_abbr', label: 'Team', sortable: true, type: 'checkbox' },
    { key: 'position', label: 'Pos', sortable: true, type: 'checkbox' },
    { key: 'salary', label: 'Salary', sortable: true, format: (val: number) => `$${val.toLocaleString()}`, type: 'range' },
    { key: 'dk_projection', label: 'Proj', sortable: true, format: (val: number) => val.toFixed(1), type: 'range' },
    { key: 'std_dev', label: 'Std Dev', sortable: true, format: (val: number) => val.toFixed(1), type: 'range' },
    { key: 'ceiling', label: 'Ceiling', sortable: true, format: (val: number) => val.toFixed(1), type: 'range' },
    { key: 'boom_pct', label: 'Boom%', sortable: true, format: (val: number) => `${val.toFixed(1)}%`, type: 'range' },
    { key: 'bust_pct', label: 'Bust%', sortable: true, format: (val: number) => `${val.toFixed(1)}%`, type: 'range' },
    { key: 'ownership_pct', label: 'Own%', sortable: true, format: (val: number) => `${val.toFixed(1)}%`, type: 'range' },
    { key: 'optimal_pct', label: 'Opt%', sortable: true, format: (val: number) => `${val.toFixed(1)}%`, type: 'range' },
    { key: 'leverage', label: 'Lev', sortable: true, format: (val: number) => val.toFixed(1), type: 'range' }
  ];

  // Get unique teams and positions
  const allTeams = useMemo(() =>
    [...new Set(players.map(p => p.team_abbr))].sort(),
    [players]
  );

  const allPositions = useMemo(() =>
    [...new Set(players.map(p => p.position))].sort(),
    [players]
  );

  // Apply column filters
  const filteredData = useMemo(() => {
    return players.filter(player => {
      // Search term filter
      if (searchTerm) {
        const matchesSearch =
          player.player_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          player.team_abbr.toLowerCase().includes(searchTerm.toLowerCase());
        if (!matchesSearch) return false;
      }

      // Position filter
      if (columnFilters.position && columnFilters.position.length > 0) {
        if (!columnFilters.position.includes(player.position)) return false;
      }

      // Team filter
      if (columnFilters.team_abbr && columnFilters.team_abbr.length > 0) {
        if (!columnFilters.team_abbr.includes(player.team_abbr)) return false;
      }

      // Range filters
      const rangeColumns: Array<keyof Player> = [
        'salary', 'dk_projection', 'std_dev', 'ceiling',
        'boom_pct', 'bust_pct', 'ownership_pct', 'optimal_pct', 'leverage'
      ];

      for (const col of rangeColumns) {
        const filter = columnFilters[col] as { min: string; max: string };
        const value = player[col] as number;
        if (filter.min !== '' && value < parseFloat(filter.min)) return false;
        if (filter.max !== '' && value > parseFloat(filter.max)) return false;
      }

      return true;
    });
  }, [players, searchTerm, columnFilters]);

  // Sort data
  const sortedData = useMemo(() => {
    if (!sortConfig.key) return filteredData;

    return [...filteredData].sort((a, b) => {
      const aVal = a[sortConfig.key as keyof Player];
      const bVal = b[sortConfig.key as keyof Player];

      if (aVal === bVal) return 0;

      const comparison = aVal < bVal ? -1 : 1;
      return sortConfig.direction === 'asc' ? comparison : -comparison;
    });
  }, [filteredData, sortConfig]);

  // Pagination
  const totalPages = Math.ceil(sortedData.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const paginatedData = sortedData.slice(startIndex, startIndex + itemsPerPage);

  // Handle sort
  const handleSort = (key: string) => {
    setSortConfig(prev => ({
      key,
      column: null,
      direction: prev.key === key && prev.direction === 'asc' ? 'desc' : 'asc'
    }));
  };

  // Toggle filter dropdown
  const toggleFilter = (key: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setActiveFilterColumn(activeFilterColumn === key ? null : key);
  };

  // Clear all filters
  const clearAllFilters = () => {
    setColumnFilters({
      searchTerm: '',
      selectedTeams: [],
      selectedPositions: [],
      position: [],
      team_abbr: [],
      salaryMin: 0,
      salaryMax: 100000,
      ownershipMin: 0,
      ownershipMax: 100,
      leverageMin: -100,
      leverageMax: 100,
      salary: { min: '', max: '' },
      dk_projection: { min: '', max: '' },
      std_dev: { min: '', max: '' },
      ceiling: { min: '', max: '' },
      boom_pct: { min: '', max: '' },
      bust_pct: { min: '', max: '' },
      ownership_pct: { min: '', max: '' },
      optimal_pct: { min: '', max: '' },
      leverage: { min: '', max: '' }
    });
    setActiveFilterColumn(null);
  };

  // Check if column has active filter
  const hasActiveFilter = (key: string): boolean => {
    if (key === 'position') return columnFilters.position ? columnFilters.position.length > 0 : false;
    if (key === 'team_abbr') return columnFilters.team_abbr ? columnFilters.team_abbr.length > 0 : false;
    const filter = columnFilters[key as keyof ColumnFilters];
    if (filter && typeof filter === 'object' && 'min' in filter) {
      return filter.min !== '' || filter.max !== '';
    }
    return false;
  };

  // Reset to page 1 when search/filters change
  useEffect(() => {
    setCurrentPage(1);
  }, [searchTerm, columnFilters]);

  return (
    <div className="data-table-container">
      <div className="table-controls">
        <div className="table-search">
          <input
            type="text"
            placeholder="Search by player name or team..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <div className="column-visibility">
          <button
            className="column-visibility-btn"
            onClick={() => setShowColumnMenu(!showColumnMenu)}
          >
            Columns ▾
          </button>
          {showColumnMenu && (
            <div className="column-visibility-dropdown">
              {columns.map(col => (
                <div
                  key={col.key}
                  className="column-visibility-item"
                  onClick={() => {
                    if (!col.locked) {
                      setVisibleColumns(prev => ({
                        ...prev,
                        [col.key]: !prev[col.key]
                      }));
                    }
                  }}
                >
                  <input
                    type="checkbox"
                    checked={visibleColumns[col.key]}
                    disabled={col.locked}
                    readOnly
                  />
                  <label>{col.label}</label>
                </div>
              ))}
            </div>
          )}
        </div>

        <button
          className="btn-secondary"
          onClick={clearAllFilters}
        >
          Clear Filters
        </button>
      </div>

      <div className="data-table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              {columns.filter(col => visibleColumns[col.key]).map(col => (
                <th
                  key={col.key}
                  className={`sortable ${sortConfig.key === col.key ? `sort-${sortConfig.direction}` : ''} ${hasActiveFilter(col.key) ? 'has-filter' : ''}`}
                >
                  <div className="th-content">
                    <span onClick={() => handleSort(col.key)}>
                      {col.label}
                      <span className="sort-indicator"></span>
                    </span>
                    {col.type !== 'text' && (
                      <button
                        className="filter-trigger"
                        onClick={(e) => toggleFilter(col.key, e)}
                        title="Filter"
                      >
                        {hasActiveFilter(col.key) ? '●' : '☰'}
                      </button>
                    )}
                  </div>

                  {/* Filter Dropdown */}
                  {activeFilterColumn === col.key && (
                    <div className="column-filter-dropdown" onClick={(e) => e.stopPropagation()}>
                      {col.type === 'checkbox' && (
                        <div className="filter-checkbox-list">
                          {(col.key === 'position' ? allPositions : allTeams).map(item => (
                            <label key={item} className="filter-checkbox-item">
                              <input
                                type="checkbox"
                                checked={(columnFilters[col.key] as string[]).includes(item)}
                                onChange={(e) => {
                                  setColumnFilters(prev => ({
                                    ...prev,
                                    [col.key]: e.target.checked
                                      ? [...(prev[col.key] as string[]), item]
                                      : (prev[col.key] as string[]).filter((x: string) => x !== item)
                                  }));
                                }}
                              />
                              {item}
                            </label>
                          ))}
                        </div>
                      )}

                      {col.type === 'range' && (
                        <div className="filter-range">
                          <div className="filter-range-item">
                            <label>Min</label>
                            <input
                              type="number"
                              placeholder="Min"
                              value={(columnFilters[col.key] as { min: string; max: string }).min}
                              onChange={(e) => {
                                setColumnFilters(prev => ({
                                  ...prev,
                                  [col.key]: {
                                    ...(prev[col.key] as { min: string; max: string }),
                                    min: e.target.value
                                  }
                                }));
                              }}
                              step={col.key === 'salary' ? '100' : '0.1'}
                            />
                          </div>
                          <div className="filter-range-item">
                            <label>Max</label>
                            <input
                              type="number"
                              placeholder="Max"
                              value={(columnFilters[col.key] as { min: string; max: string }).max}
                              onChange={(e) => {
                                setColumnFilters(prev => ({
                                  ...prev,
                                  [col.key]: {
                                    ...(prev[col.key] as { min: string; max: string }),
                                    max: e.target.value
                                  }
                                }));
                              }}
                              step={col.key === 'salary' ? '100' : '0.1'}
                            />
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {paginatedData.map((player, idx) => (
              <tr key={`${player.player_id}_${idx}`}>
                {columns.filter(col => visibleColumns[col.key]).map(col => (
                  <td key={col.key}>
                    {col.key === 'player_name' ? (
                      <div className="player-cell">
                        <img
                          src={player.headshot_url}
                          className="player-headshot"
                          alt={player.player_name}
                          loading="lazy"
                          style={{ borderColor: getTeamColor(player.team_abbr) }}
                          onError={(e) => { (e.target as HTMLImageElement).style.display = 'none'; }}
                        />
                        <span className="player-name">{player.player_name}</span>
                      </div>
                    ) : col.key === 'team_abbr' ? (
                      <div className="team-cell">
                        <img
                          src={getTeamLogoUrl(player.team_abbr)}
                          className="team-logo"
                          alt={player.team_abbr}
                          title={player.team_abbr}
                          loading="lazy"
                        />
                      </div>
                    ) : col.key === 'position' ? (
                      <span className={`position-badge position-${player.position}`}>
                        {player.position}
                      </span>
                    ) : col.format ? (
                      col.format(player[col.key] as number)
                    ) : (
                      player[col.key]
                    )}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="pagination">
        <div className="pagination-info">
          Showing {startIndex + 1}-{Math.min(startIndex + itemsPerPage, sortedData.length)} of {sortedData.length} players
        </div>
        <div className="pagination-buttons">
          <button
            className="pagination-button"
            onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
            disabled={currentPage === 1}
          >
            Previous
          </button>
          <span className="pagination-info">Page {currentPage} of {totalPages}</span>
          <button
            className="pagination-button"
            onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
            disabled={currentPage === totalPages}
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
};

export default DataTable;
