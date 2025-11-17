import type { Position } from '../../types/player';
import { POSITIONS } from '../../types/player';
import './PositionFilter.css';
import './Filters.css';

interface PositionFilterProps {
  selectedPositions: Position[];
  onTogglePosition: (position: Position) => void;
}

const PositionFilter = ({
  selectedPositions,
  onTogglePosition
}: PositionFilterProps) => {
  return (
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
  );
};

export default PositionFilter;
