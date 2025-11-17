import React from 'react';

interface RangeFilterProps {
  label: string;
  min: number;
  max: number;
  step: number;
  value: [number, number];
  onChange: (value: [number, number]) => void;
  formatValue?: (value: number) => string;
}

const RangeFilter: React.FC<RangeFilterProps> = ({
  label,
  min,
  max,
  step,
  value,
  onChange,
  formatValue = (v) => v.toString()
}) => {
  const handleMinChange = (newMin: number) => {
    if (newMin < value[1]) {
      onChange([newMin, value[1]]);
    }
  };

  const handleMaxChange = (newMax: number) => {
    if (newMax > value[0]) {
      onChange([value[0], newMax]);
    }
  };

  return (
    <div className="filter-item">
      <label>{label}</label>
      <div className="range-values">
        <span>{formatValue(value[0])}</span>
        <span>{formatValue(value[1])}</span>
      </div>
      <div className="slider-container">
        <input
          type="range"
          min={min}
          max={max}
          step={step}
          value={value[0]}
          onChange={(e) => handleMinChange(parseInt(e.target.value))}
        />
        <input
          type="range"
          min={min}
          max={max}
          step={step}
          value={value[1]}
          onChange={(e) => handleMaxChange(parseInt(e.target.value))}
        />
      </div>
    </div>
  );
};

export default RangeFilter;
