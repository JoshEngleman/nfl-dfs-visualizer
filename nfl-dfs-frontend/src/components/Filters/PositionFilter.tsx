import React from 'react';
import { Position, POSITIONS } from '../../types/player';

interface PositionFilterProps {
  selectedPositions: Position[];
  onTogglePosition: (position: Position) => void;
}

const PositionFilter: React.FC<PositionFilterProps> = ({
  selectedPositions,
  onTogglePosition
}) => {
  return (
    <div className="filter-group">
      <div className="filter-group-header">Positions</div>
      <div className="filter-group-content">
        <div className="position-badges-container">
          {POSITIONS.map(pos => (
            <div
              key={pos}
              className={`position-toggle position-${pos} ${
                selectedPositions.includes(pos) ? 'active' : 'inactive'
              }`}
              onClick={() => onTogglePosition(pos)}
            >
              {pos}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PositionFilter;
