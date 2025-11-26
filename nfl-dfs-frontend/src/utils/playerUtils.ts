/**
 * Player utility functions including name mappings and headshot fetching
 */

import type { Player } from '../types/player';

// Name mappings for players with suffixes (Sr., Jr., III, etc.)
export const NAME_MAPPINGS: { [key: string]: string } = {
  "Kyle Pitts Sr.|ATL": "Kyle Pitts",
  "Aaron Jones Sr.|MIN": "Aaron Jones",
  "James Cook III|BUF": "James Cook",
  "Ray-Ray McCloud III|NYG": "Ray-Ray McCloud"
};

/**
 * Apply name mapping for players with suffixes
 */
export const applyNameMapping = (playerName: string, teamAbbr: string): string => {
  const mappingKey = `${playerName}|${teamAbbr}`;
  return NAME_MAPPINGS[mappingKey] || playerName;
};

/**
 * Clean player name for use in URLs (remove special characters, replace spaces with underscores)
 */
export const cleanPlayerName = (name: string): string => {
  return name.replace(/[^a-zA-Z0-9\s]/g, '').replace(/\s+/g, '_');
};

/**
 * Get headshot URL for a player
 * Uses local headshots from /nfl-dfs/headshots/
 */
export const getHeadshotUrl = (player: Player): string => {
  // For DST, use team logo
  if (player.position === 'DST') {
    return `https://a.espncdn.com/i/teamlogos/nfl/500/${player.team_abbr.toUpperCase()}.png`;
  }

  const nameToUse = applyNameMapping(player.player_name, player.team_abbr);
  const cleanName = cleanPlayerName(nameToUse);

  return `/nfl-dfs/headshots/${cleanName}.png`;
};

/**
 * Get fallback headshot URL (team logo)
 */
export const getFallbackHeadshotUrl = (teamAbbr: string): string => {
  return `https://a.espncdn.com/i/teamlogos/nfl/500/${teamAbbr.toLowerCase()}.png`;
};

/**
 * Format currency (salary)
 */
export const formatSalary = (salary: number): string => {
  return `$${salary.toLocaleString()}`;
};

/**
 * Format percentage
 */
export const formatPercentage = (value: number): string => {
  return `${value.toFixed(1)}%`;
};

/**
 * Format decimal number
 */
export const formatDecimal = (value: number, decimals: number = 1): string => {
  return value.toFixed(decimals);
};

/**
 * Get position color (for badges)
 */
export const getPositionColor = (position: string): string => {
  const colors: { [key: string]: string } = {
    'QB': '#dc2626',
    'RB': '#059669',
    'WR': '#3b82f6',
    'TE': '#d97706',
    'DST': '#6b7280',
    'ALL': '#8b5cf6'
  };
  return colors[position] || '#6b7280';
};
