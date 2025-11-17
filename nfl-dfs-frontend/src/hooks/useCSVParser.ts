/**
 * Hook for parsing CSV files with Papa Parse
 */

import { useState } from 'react';
import Papa from 'papaparse';
import { Player, CSVParseResult, StoredData } from '../types/player';
import { getHeadshotUrl } from '../utils/playerUtils';

export const useCSVParser = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const parseCSV = (file: File): Promise<CSVParseResult> => {
    return new Promise((resolve) => {
      setIsLoading(true);
      setError(null);

      Papa.parse(file, {
        header: true,
        skipEmptyLines: true,
        complete: (results) => {
          try {
            const players: Player[] = results.data.map((row: any) => {
              const player: Player = {
                player_name: row.Name || row.player_name || '',
                player_id: row['Name + ID'] || row.player_id || `${row.Name}_${Date.now()}`,
                position: row.Position || row.position || 'ALL',
                team_abbr: row.TeamAbbrev || row.team_abbr || '',
                salary: parseFloat(row.Salary || row.salary || '0'),
                dk_projection: parseFloat(row['DK Projection'] || row.dk_projection || '0'),
                std_dev: parseFloat(row['Std Dev'] || row.std_dev || '0'),
                ceiling: parseFloat(row.Ceiling || row.ceiling || '0'),
                bust_pct: parseFloat(row['Bust%'] || row.bust_pct || '0'),
                boom_pct: parseFloat(row['Boom%'] || row.boom_pct || '0'),
                ownership_pct: parseFloat(row['Ownership%'] || row.ownership_pct || '0'),
                optimal_pct: parseFloat(row['Optimal%'] || row.optimal_pct || '0'),
                leverage: parseFloat(row.Leverage || row.leverage || '0'),
                headshot_url: ''
              };

              // Generate headshot URL
              player.headshot_url = getHeadshotUrl(player);

              return player;
            }).filter(player => player.player_name); // Filter out empty rows

            // Group by position
            const grouped: StoredData = {
              ALL: players
            };

            ['QB', 'RB', 'WR', 'TE', 'DST'].forEach(pos => {
              grouped[pos] = players.filter(p => p.position === pos);
            });

            setIsLoading(false);
            resolve({
              data: players,
              errors: results.errors.map(e => e.message),
              success: true
            });
          } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Unknown error parsing CSV';
            setError(errorMessage);
            setIsLoading(false);
            resolve({
              data: [],
              errors: [errorMessage],
              success: false
            });
          }
        },
        error: (err) => {
          const errorMessage = err.message || 'Failed to parse CSV file';
          setError(errorMessage);
          setIsLoading(false);
          resolve({
            data: [],
            errors: [errorMessage],
            success: false
          });
        }
      });
    });
  };

  return {
    parseCSV,
    isLoading,
    error
  };
};
