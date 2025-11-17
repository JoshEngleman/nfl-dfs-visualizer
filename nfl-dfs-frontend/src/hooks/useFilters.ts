/**
 * Hook for managing filter state (chart and table)
 */

import { useState } from 'react';
import { Position, Player } from '../types/player';

export interface FilterState {
  position: Position;
  selectedTeams: string[];
  ownershipRange: [number, number];
  projectionRange: [number, number];
  salaryRange: [number, number];
  leverageRange: [number, number];
}

const DEFAULT_FILTERS: FilterState = {
  position: 'ALL',
  selectedTeams: [],
  ownershipRange: [0, 100],
  projectionRange: [0, 100],
  salaryRange: [3000, 10000],
  leverageRange: [-100, 100]
};

export const useFilters = () => {
  const [filters, setFilters] = useState<FilterState>(DEFAULT_FILTERS);

  /**
   * Update position filter
   */
  const setPosition = (position: Position) => {
    setFilters(prev => ({ ...prev, position }));
  };

  /**
   * Toggle team selection
   */
  const toggleTeam = (team: string) => {
    setFilters(prev => ({
      ...prev,
      selectedTeams: prev.selectedTeams.includes(team)
        ? prev.selectedTeams.filter(t => t !== team)
        : [...prev.selectedTeams, team]
    }));
  };

  /**
   * Clear all team selections
   */
  const clearTeams = () => {
    setFilters(prev => ({ ...prev, selectedTeams: [] }));
  };

  /**
   * Select all teams
   */
  const selectAllTeams = (teams: string[]) => {
    setFilters(prev => ({ ...prev, selectedTeams: teams }));
  };

  /**
   * Update ownership range
   */
  const setOwnershipRange = (range: [number, number]) => {
    setFilters(prev => ({ ...prev, ownershipRange: range }));
  };

  /**
   * Update projection range
   */
  const setProjectionRange = (range: [number, number]) => {
    setFilters(prev => ({ ...prev, projectionRange: range }));
  };

  /**
   * Update salary range
   */
  const setSalaryRange = (range: [number, number]) => {
    setFilters(prev => ({ ...prev, salaryRange: range }));
  };

  /**
   * Update leverage range
   */
  const setLeverageRange = (range: [number, number]) => {
    setFilters(prev => ({ ...prev, leverageRange: range }));
  };

  /**
   * Reset all filters to defaults
   */
  const resetFilters = () => {
    setFilters(DEFAULT_FILTERS);
  };

  /**
   * Apply filters to player data
   */
  const applyFilters = (players: Player[]): Player[] => {
    return players.filter(player => {
      // Position filter
      if (filters.position !== 'ALL' && player.position !== filters.position) {
        return false;
      }

      // Team filter
      if (filters.selectedTeams.length > 0 && !filters.selectedTeams.includes(player.team_abbr)) {
        return false;
      }

      // Ownership range
      if (player.ownership_pct < filters.ownershipRange[0] || player.ownership_pct > filters.ownershipRange[1]) {
        return false;
      }

      // Projection range
      if (player.dk_projection < filters.projectionRange[0] || player.dk_projection > filters.projectionRange[1]) {
        return false;
      }

      // Salary range
      if (player.salary < filters.salaryRange[0] || player.salary > filters.salaryRange[1]) {
        return false;
      }

      // Leverage range
      if (player.leverage < filters.leverageRange[0] || player.leverage > filters.leverageRange[1]) {
        return false;
      }

      return true;
    });
  };

  return {
    filters,
    setPosition,
    toggleTeam,
    clearTeams,
    selectAllTeams,
    setOwnershipRange,
    setProjectionRange,
    setSalaryRange,
    setLeverageRange,
    resetFilters,
    applyFilters
  };
};
