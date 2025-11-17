/**
 * Hook for managing player data state
 */

import { useState, useEffect } from 'react';
import { Player, StoredData, Position } from '../types/player';
import { saveToLocalStorage, loadFromLocalStorage, hasStoredData } from '../utils/storage';

export const usePlayerData = () => {
  const [allData, setAllData] = useState<StoredData | null>(null);
  const [currentPosition, setCurrentPosition] = useState<Position>('ALL');
  const [players, setPlayers] = useState<Player[]>([]);

  // Load data from localStorage on mount
  useEffect(() => {
    const stored = loadFromLocalStorage();
    if (stored) {
      setAllData(stored);
      setPlayers(stored.ALL || []);
    }
  }, []);

  // Update players when position changes
  useEffect(() => {
    if (allData) {
      setPlayers(allData[currentPosition] || []);
    }
  }, [currentPosition, allData]);

  /**
   * Set new player data (from CSV upload)
   */
  const setPlayerData = (data: StoredData) => {
    setAllData(data);
    setPlayers(data[currentPosition] || []);
    saveToLocalStorage(data);
  };

  /**
   * Clear all player data
   */
  const clearData = () => {
    setAllData(null);
    setPlayers([]);
    setCurrentPosition('ALL');
    localStorage.removeItem('nflDfsUploadedData');
  };

  /**
   * Change current position filter
   */
  const changePosition = (position: Position) => {
    setCurrentPosition(position);
  };

  /**
   * Check if data exists
   */
  const hasData = (): boolean => {
    return allData !== null && players.length > 0;
  };

  /**
   * Get players for a specific position
   */
  const getPlayersByPosition = (position: Position): Player[] => {
    return allData?.[position] || [];
  };

  return {
    allData,
    players,
    currentPosition,
    setPlayerData,
    clearData,
    changePosition,
    hasData,
    getPlayersByPosition,
    hasStoredData: hasStoredData()
  };
};
