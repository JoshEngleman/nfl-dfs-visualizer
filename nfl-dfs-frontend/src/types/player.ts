/**
 * TypeScript type definitions for NFL DFS Visualizer
 * Based on data structure from existing index.html
 */

// Main player data interface
export interface Player {
  player_name: string;
  player_id: string;
  position: Position;
  team_abbr: string;
  salary: number;
  dk_projection: number;
  projection: number;
  proj_ownership: number;
  pts_per_dollar: number;
  std_dev: number;
  ceiling: number;
  bust_pct: number;
  boom_pct: number;
  ownership_pct: number;
  optimal_pct: number;
  leverage: number;
  headshot_url: string;
}

// Position types
export type Position = 'QB' | 'RB' | 'WR' | 'TE' | 'DST' | 'ALL';

// Available positions for filtering
export const POSITIONS: Position[] = ['ALL', 'QB', 'RB', 'WR', 'TE', 'DST'];

// All NFL teams
export const NFL_TEAMS = [
  'ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE',
  'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC',
  'LAC', 'LAR', 'LV', 'MIA', 'MIN', 'NE', 'NO', 'NYG',
  'NYJ', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN', 'WAS'
] as const;

export type NFLTeam = typeof NFL_TEAMS[number];

// Chart data type (for scatter plot)
export interface ChartData {
  x: number;
  y: number;
  z: number;
  leverage: number;
  boom_pct: number;
  ownership_pct: number;
  player_name: string;
  position: Position;
  team_abbr: string;
  salary: number;
  dk_projection: number;
  projection: number;
  proj_ownership: number;
  pts_per_dollar: number;
  std_dev: number;
  ceiling: number;
  bust_pct: number;
  optimal_pct: number;
  headshot_url: string;
}

// Filter state for chart view
export interface ChartFilters {
  position: Position;
  selectedTeams: string[];
  ownershipRange: [number, number];
  projectionRange: [number, number];
  salaryRange: [number, number];
  leverageRange: [number, number];
}

// Table column definition
export interface TableColumn {
  key: keyof Player;
  label: string;
  sortable: boolean;
  locked?: boolean;
  type?: string;
  format?: (val: number) => string;
}

// Table sort state
export interface TableSort {
  key?: string;
  column: keyof Player | null;
  direction: 'asc' | 'desc';
}

// Data stored in localStorage
export interface StoredData {
  ALL: Player[];
  [key: string]: Player[]; // Allows QB, RB, etc. as keys
}

// View mode
export type ViewMode = 'chart' | 'table';

// Column visibility state (for data table)
export type ColumnVisibility = {
  [key in keyof Player]?: boolean;
};

// Column filter state (for data table)
export interface ColumnFilters {
  searchTerm: string;
  selectedTeams: string[];
  selectedPositions: Position[];
  position?: Position[];
  team_abbr?: string[];
  salaryMin: number;
  salaryMax: number;
  ownershipMin: number;
  ownershipMax: number;
  leverageMin: number;
  leverageMax: number;
  min?: number;
  max?: number;
  [key: string]: any;
}

// CSV parser result
export interface CSVParseResult {
  data: Player[];
  errors: string[];
  success: boolean;
}

// Team colors mapping
export interface TeamColors {
  [team: string]: string;
}

// Name mapping for player headshots
export interface NameMapping {
  mappings: {
    [key: string]: string;
  };
}
