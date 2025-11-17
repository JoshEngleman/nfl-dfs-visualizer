/**
 * CSV Upload Component
 * Allows users to upload and parse DraftKings CSV files
 */

import React, { useRef } from 'react';
import { useCSVParser } from '../../hooks/useCSVParser';
import { StoredData } from '../../types/player';
import './CSVUpload.css';

interface CSVUploadProps {
  onDataLoaded: (data: StoredData) => void;
}

export const CSVUpload: React.FC<CSVUploadProps> = ({ onDataLoaded }) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { parseCSV, isLoading, error } = useCSVParser();

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    try {
      const result = await parseCSV(file);

      if (result.success && result.data.length > 0) {
        // Group data by position
        const grouped: StoredData = {
          ALL: result.data
        };

        ['QB', 'RB', 'WR', 'TE', 'DST'].forEach(pos => {
          grouped[pos] = result.data.filter(p => p.position === pos);
        });

        onDataLoaded(grouped);
      } else {
        alert(`Failed to parse CSV: ${result.errors.join(', ')}`);
      }
    } catch (err) {
      console.error('Error parsing CSV:', err);
      alert('Failed to parse CSV file. Please check the file format.');
    }

    // Reset file input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="upload-container">
      <input
        ref={fileInputRef}
        type="file"
        accept=".csv"
        onChange={handleFileChange}
        style={{ display: 'none' }}
      />
      <button
        onClick={handleClick}
        disabled={isLoading}
        className="upload-button"
      >
        {isLoading ? 'Uploading...' : 'Upload CSV'}
      </button>
      {error && (
        <div className="error-message">
          Error: {error}
        </div>
      )}
    </div>
  );
};
