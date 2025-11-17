/**
 * Team colors and logo utilities for NFL teams
 */

import type { TeamColors } from '../types/player';

export const TEAM_COLORS: TeamColors = {
  'ARI': '#97233F',
  'ATL': '#A71930',
  'BAL': '#241773',
  'BUF': '#00338D',
  'CAR': '#0085CA',
  'CHI': '#C83803',
  'CIN': '#FB4F14',
  'CLE': '#311D00',
  'DAL': '#041E42',
  'DEN': '#FB4F14',
  'DET': '#0076B6',
  'GB': '#203731',
  'HOU': '#03202F',
  'IND': '#002C5F',
  'JAX': '#006778',
  'KC': '#E31837',
  'LAC': '#0080C6',
  'LAR': '#003594',
  'LV': '#000000',
  'MIA': '#008E97',
  'MIN': '#4F2683',
  'NE': '#002244',
  'NO': '#D3BC8D',
  'NYG': '#0B2265',
  'NYJ': '#125740',
  'PHI': '#004C54',
  'PIT': '#FFB612',
  'SF': '#AA0000',
  'SEA': '#002244',
  'TB': '#D50A0A',
  'TEN': '#0C2340',
  'WAS': '#5A1414'
};

/**
 * Get team color for a given team abbreviation
 */
export const getTeamColor = (teamAbbr: string): string => {
  return TEAM_COLORS[teamAbbr] || '#6b7280'; // Default gray if team not found
};

/**
 * Get team logo URL from ESPN
 */
export const getTeamLogoUrl = (teamAbbr: string): string => {
  return `https://a.espncdn.com/i/teamlogos/nfl/500/${teamAbbr.toLowerCase()}.png`;
};
