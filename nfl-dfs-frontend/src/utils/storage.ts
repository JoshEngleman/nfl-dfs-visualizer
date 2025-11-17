/**
 * LocalStorage utilities for persisting player data
 */

import { Player, StoredData } from '../types/player';

const STORAGE_KEY = 'nflDfsUploadedData';

/**
 * Save player data to localStorage
 */
export const saveToLocalStorage = (data: StoredData): void => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  } catch (error) {
    console.error('Failed to save to localStorage:', error);
  }
};

/**
 * Load player data from localStorage
 */
export const loadFromLocalStorage = (): StoredData | null => {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      return JSON.parse(stored);
    }
  } catch (error) {
    console.error('Failed to load from localStorage:', error);
  }
  return null;
};

/**
 * Clear player data from localStorage
 */
export const clearLocalStorage = (): void => {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch (error) {
    console.error('Failed to clear localStorage:', error);
  }
};

/**
 * Check if localStorage has data
 */
export const hasStoredData = (): boolean => {
  return localStorage.getItem(STORAGE_KEY) !== null;
};
