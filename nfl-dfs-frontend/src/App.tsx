import { useState, useEffect, useMemo } from 'react';
import type { Player, Position, ViewMode } from './types/player';
import { hasStoredData, loadFromLocalStorage } from './utils/storage';
import { CSVUpload } from './components/Upload/CSVUpload';
import ChartView from './components/Chart/ChartView';
import DataTable from './components/DataTable/DataTable';
import { PositionFilter, TeamFilter, RangeFilter } from './components/Filters';
import './App.css';

const DEFAULT_POSITION: Position = 'ALL';

function App() {
  // View state
  const [activeTab, setActiveTab] = useState<ViewMode>('chart');
  const [allData, setAllData] = useState<Record<Position, Player[]>>({
    ALL: [],
    QB: [],
    RB: [],
    WR: [],
    TE: [],
    DST: []
  });

  // Position filter (multi-select)
  const [selectedPositions, setSelectedPositions] = useState<Position[]>([DEFAULT_POSITION]);
  const [players, setPlayers] = useState<Player[]>([]);

  // Additional filters
  const [selectedTeams, setSelectedTeams] = useState<string[]>([]);
  const [salaryRange, setSalaryRange] = useState<[number, number]>([3000, 12000]);
  const [ownershipRange, setOwnershipRange] = useState<[number, number]>([0, 100]);

  // Load data from localStorage on mount
  useEffect(() => {
    if (hasStoredData()) {
      const stored = loadFromLocalStorage();
      if (stored) {
        setAllData(stored as any);
      }
    }
  }, []);

  // Update players when selectedPositions change
  useEffect(() => {
    if (selectedPositions.length === 0) {
      setPlayers([]);
      return;
    }

    // If 'ALL' is selected, use only the ALL dataset
    if (selectedPositions.includes('ALL')) {
      setPlayers(allData['ALL'] || []);
      return;
    }

    // Otherwise, combine data from selected positions and remove duplicates
    const combined = selectedPositions.flatMap(pos => allData[pos] || []);
    const uniquePlayers = combined.filter((player, index, self) =>
      index === self.findIndex(p => p.player_id === player.player_id)
    );
    setPlayers(uniquePlayers);
  }, [selectedPositions, allData]);

  // Extract unique teams from ALL players
  const allTeams = useMemo(() => {
    const allTeamsData = allData['ALL'] || [];
    return [...new Set(allTeamsData.map(p => p.team_abbr))].sort();
  }, [allData]);

  // Apply filters
  const filteredPlayers = useMemo(() => {
    return players.filter(p => {
      // Team filter
      if (selectedTeams.length > 0 && !selectedTeams.includes(p.team_abbr)) {
        return false;
      }
      // Salary filter
      if (p.salary < salaryRange[0] || p.salary > salaryRange[1]) {
        return false;
      }
      // Ownership filter
      if (p.ownership_pct < ownershipRange[0] || p.ownership_pct > ownershipRange[1]) {
        return false;
      }
      return true;
    });
  }, [players, selectedTeams, salaryRange, ownershipRange]);

  // Handle position toggle
  const togglePosition = (position: Position) => {
    setSelectedPositions(prev => {
      // If clicking ALL, select only ALL
      if (position === 'ALL') {
        return ['ALL'];
      }

      // If ALL is currently selected, replace with clicked position
      if (prev.includes('ALL')) {
        return [position];
      }

      // Toggle position
      if (prev.includes(position)) {
        const newPositions = prev.filter(p => p !== position);
        // If no positions left, select ALL
        return newPositions.length === 0 ? ['ALL'] : newPositions;
      } else {
        return [...prev, position];
      }
    });
  };

  // Handle team toggle
  const toggleTeam = (team: string) => {
    setSelectedTeams(prev =>
      prev.includes(team)
        ? prev.filter(t => t !== team)
        : [...prev, team]
    );
  };

  // Handle CSV upload
  const handleDataParsed = (parsedData: Record<Position, Player[]> | any) => {
    setAllData(parsedData);
    setSelectedPositions([DEFAULT_POSITION]);
  };

  const hasData = allData.ALL.length > 0;

  return (
    <div className="app">
      <header className="header">
        <h1>🏈 NFL DFS Boom/Bust Visualizer</h1>
        <CSVUpload onDataLoaded={handleDataParsed} />
      </header>

      {!hasData ? (
        <div className="empty-state">
          <p>Upload a CSV file to get started</p>
        </div>
      ) : (
        <>
          {/* Tab Navigation */}
          <div className="tabs">
            <button
              className={`tab-button ${activeTab === 'chart' ? 'active' : ''}`}
              onClick={() => setActiveTab('chart')}
            >
              Chart View
            </button>
            <button
              className={`tab-button ${activeTab === 'table' ? 'active' : ''}`}
              onClick={() => setActiveTab('table')}
            >
              Data Table
            </button>
          </div>

          {/* Chart Tab Content */}
          <div className={`tab-content ${activeTab === 'chart' ? 'active' : ''}`}>
            <div className="filters-container">
              {/* Group 1: Position & Player Filters */}
              <div className="filter-group">
                <PositionFilter
                  selectedPositions={selectedPositions}
                  onTogglePosition={togglePosition}
                />

                <div className="filter-group-content">
                  <RangeFilter
                    label="Salary Range"
                    min={3000}
                    max={12000}
                    step={100}
                    value={salaryRange}
                    onChange={setSalaryRange}
                    formatValue={(v) => `$${(v / 1000).toFixed(1)}K`}
                  />

                  <RangeFilter
                    label="Ownership Range"
                    min={0}
                    max={100}
                    step={1}
                    value={ownershipRange}
                    onChange={setOwnershipRange}
                    formatValue={(v) => `${v}%`}
                  />
                </div>
              </div>

              {/* Group 2: Team Filters */}
              <TeamFilter
                allTeams={allTeams}
                selectedTeams={selectedTeams}
                onToggleTeam={toggleTeam}
              />
            </div>

            {/* Chart Component */}
            <ChartView players={filteredPlayers} />
          </div>

          {/* Table Tab Content */}
          <div className={`tab-content ${activeTab === 'table' ? 'active' : ''}`}>
            <DataTable players={allData.ALL} />
          </div>
        </>
      )}
    </div>
  );
}

export default App;
