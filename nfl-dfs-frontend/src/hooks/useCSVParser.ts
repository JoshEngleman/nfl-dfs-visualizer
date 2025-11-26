/**
 * Hook for parsing CSV files with Papa Parse
 */

import { useState } from 'react';
import Papa from 'papaparse';
import type { Player, CSVParseResult, StoredData } from '../types/player';
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
        transformHeader: (header: string) => header.trim(),
        complete: (results) => {
          try {
            // Log headers for debugging
            if (results.data.length > 0) {
              const firstRow = results.data[0] as Record<string, unknown>;
              console.log('CSV Headers:', Object.keys(firstRow));
              console.log('First row:', firstRow);
            }

            const players: Player[] = results.data.map((row: any) => {
              // Helper to get value by trying multiple possible column names
              const getValue = (...keys: string[]): string => {
                for (const key of keys) {
                  if (row[key] !== undefined && row[key] !== null && row[key] !== '') {
                    return String(row[key]);
                  }
                }
                return '';
              };

              // Handle salary with commas (e.g., "8,100")
              const salaryStr = getValue('Salary', 'salary');
              const salary = parseFloat(salaryStr.replace(/,/g, '')) || 0;

              const projection = parseFloat(getValue('Projection', 'DK Projection', 'dk_projection', 'projection')) || 0;
              const ownership = parseFloat(getValue('Own%', 'Ownership%', 'ownership_pct', 'proj_ownership')) || 0;

              const player: Player = {
                player_name: getValue('Name', 'player_name'),
                player_id: getValue('Name + ID', 'player_id') || `${getValue('Name', 'player_name')}_${Date.now()}_${Math.random()}`,
                position: getValue('Position', 'position') as any || 'ALL',
                team_abbr: getValue('Team', 'TeamAbbrev', 'team_abbr'),
                salary: salary,
                dk_projection: projection,
                projection: projection,
                proj_ownership: ownership,
                pts_per_dollar: salary > 0 ? projection / (salary / 1000) : 0,
                std_dev: parseFloat(getValue('Std Dev', 'std_dev')) || 0,
                ceiling: parseFloat(getValue('Ceiling', 'ceiling')) || 0,
                bust_pct: parseFloat(getValue('Bust%', 'bust_pct')) || 0,
                boom_pct: parseFloat(getValue('Boom%', 'boom_pct')) || 0,
                ownership_pct: ownership,
                optimal_pct: parseFloat(getValue('Optimal%', 'optimal_pct')) || 0,
                leverage: parseFloat(getValue('Leverage', 'leverage')) || 0,
                headshot_url: ''
              };

              console.log('Parsed player:', player.player_name, 'Team:', player.team_abbr, 'Salary:', player.salary, 'Proj:', player.projection);

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
