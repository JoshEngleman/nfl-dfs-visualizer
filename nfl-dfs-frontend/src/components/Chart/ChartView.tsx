import { useState, useMemo } from 'react';
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
  ReferenceArea,
} from 'recharts';
import type { Player, ChartData } from '../../types/player';
import { getTeamColor } from '../../utils/teamColors';
import PlayerTooltip from './PlayerTooltip';
import PlayerHeadshot from './PlayerHeadshot';
import './ChartView.css';

interface ChartViewProps {
  players: Player[];
}

interface StatOption {
  value: string;
  label: string;
}

const statOptions: StatOption[] = [
  { value: 'boom_pct', label: 'Boom%' },
  { value: 'proj_ownership', label: 'Proj Own%' },
  { value: 'projection', label: 'Projection' },
  { value: 'salary', label: 'Salary' },
  { value: 'leverage', label: 'Leverage' },
  { value: 'pts_per_dollar', label: 'Pts/$' },
];

export default function ChartView({ players }: ChartViewProps) {
  // Axis configuration
  const [xAxisStat, setXAxisStat] = useState('boom_pct');
  const [yAxisStat, setYAxisStat] = useState('leverage');
  const [sizeStat, setSizeStat] = useState('proj_ownership');

  // Zoom state
  const [left, setLeft] = useState<number | null>(null);
  const [right, setRight] = useState<number | null>(null);
  const [top, setTop] = useState<number | null>(null);
  const [bottom, setBottom] = useState<number | null>(null);
  const [refAreaLeft, setRefAreaLeft] = useState<number | null>(null);
  const [refAreaRight, setRefAreaRight] = useState<number | null>(null);
  const [refAreaTop, setRefAreaTop] = useState<number | null>(null);
  const [refAreaBottom, setRefAreaBottom] = useState<number | null>(null);

  // Calculate chart data
  const chartData: ChartData[] = useMemo(() => {
    return players.map((player) => ({
      x: player[xAxisStat as keyof Player] as number,
      y: player[yAxisStat as keyof Player] as number,
      z: player[sizeStat as keyof Player] as number,
      player_name: player.player_name,
      position: player.position,
      team_abbr: player.team_abbr,
      salary: player.salary,
      projection: player.projection,
      proj_ownership: player.proj_ownership,
      boom_pct: player.boom_pct,
      leverage: player.leverage,
      pts_per_dollar: player.pts_per_dollar,
      headshot_url: player.headshot_url,
    }));
  }, [players, xAxisStat, yAxisStat, sizeStat]);

  // Calculate default bounds and median
  const { defaultLeft, defaultRight, defaultTop, defaultBottom, xMedian } = useMemo(() => {
    if (chartData.length === 0) {
      return { defaultLeft: 0, defaultRight: 100, defaultTop: 10, defaultBottom: -10, xMedian: 50 };
    }

    const xValues = chartData.map((d) => d.x).filter((v) => v != null);
    const yValues = chartData.map((d) => d.y).filter((v) => v != null);

    const xMin = Math.min(...xValues);
    const xMax = Math.max(...xValues);
    const yMin = Math.min(...yValues);
    const yMax = Math.max(...yValues);

    const xPadding = (xMax - xMin) * 0.1;
    const yPadding = (yMax - yMin) * 0.1;

    const sortedX = [...xValues].sort((a, b) => a - b);
    const median = sortedX[Math.floor(sortedX.length / 2)];

    return {
      defaultLeft: xMin - xPadding,
      defaultRight: xMax + xPadding,
      defaultTop: yMax + yPadding,
      defaultBottom: yMin - yPadding,
      xMedian: median,
    };
  }, [chartData]);

  // Get axis labels
  const getStatLabel = (stat: string): string => {
    return statOptions.find((s) => s.value === stat)?.label || stat;
  };

  const xAxisLabel = getStatLabel(xAxisStat);
  const yAxisLabel = getStatLabel(yAxisStat);
  const sizeLabel = getStatLabel(sizeStat);

  // Zoom handlers
  const zoom = () => {
    if (refAreaLeft === null || refAreaRight === null) {
      return;
    }

    // Get zoom area bounds
    let newLeft = Math.min(refAreaLeft, refAreaRight);
    let newRight = Math.max(refAreaLeft, refAreaRight);
    let newBottom = Math.min(refAreaTop!, refAreaBottom!);
    let newTop = Math.max(refAreaTop!, refAreaBottom!);

    // Reset ref area
    setRefAreaLeft(null);
    setRefAreaRight(null);
    setRefAreaTop(null);
    setRefAreaBottom(null);

    // Apply zoom
    setLeft(newLeft);
    setRight(newRight);
    setBottom(newBottom);
    setTop(newTop);
  };

  const zoomOut = () => {
    setLeft(null);
    setRight(null);
    setTop(null);
    setBottom(null);
    setRefAreaLeft(null);
    setRefAreaRight(null);
    setRefAreaTop(null);
    setRefAreaBottom(null);
  };

  return (
    <div className="chart-container">
      {/* Chart Configuration */}
      <div className="chart-controls">
        <div className="control-group">
          <label>X-Axis</label>
          <select value={xAxisStat} onChange={(e) => setXAxisStat(e.target.value)}>
            {statOptions.map((stat) => (
              <option key={stat.value} value={stat.value}>
                {stat.label}
              </option>
            ))}
          </select>
        </div>

        <div className="control-group">
          <label>Y-Axis</label>
          <select value={yAxisStat} onChange={(e) => setYAxisStat(e.target.value)}>
            {statOptions.map((stat) => (
              <option key={stat.value} value={stat.value}>
                {stat.label}
              </option>
            ))}
          </select>
        </div>

        <div className="control-group">
          <label>Bubble Size</label>
          <select value={sizeStat} onChange={(e) => setSizeStat(e.target.value)}>
            {statOptions.map((stat) => (
              <option key={stat.value} value={stat.value}>
                {stat.label}
              </option>
            ))}
          </select>
        </div>

        <button className="btn-primary" onClick={zoomOut}>
          Reset Zoom
        </button>
      </div>

      {/* Chart Info */}
      <div className="chart-info">
        {players.length} players • Median {xAxisLabel}: {xMedian.toFixed(1)} | {yAxisLabel} at 0
        <br />
        Size = {sizeLabel} | Color = Quadrant (🟢 Best, 🟡 Contrarian, ⚪ Popular, 🔴 Avoid) | Drag to
        zoom, Reset Zoom to clear
      </div>

      {/* Chart */}
      <div className="chart-wrapper">
        <ResponsiveContainer width="100%" height={700}>
          <ScatterChart
            margin={{ top: 40, right: 120, bottom: 60, left: 60 }}
            onMouseDown={(e: any) => {
              if (e) {
                setRefAreaLeft(e.xValue);
                setRefAreaTop(e.yValue);
              }
            }}
            onMouseMove={(e: any) => {
              if (refAreaLeft && e) {
                setRefAreaRight(e.xValue);
                setRefAreaBottom(e.yValue);
              }
            }}
            onMouseUp={zoom}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#d1d5db" strokeWidth={1.5} />
            <XAxis
              type="number"
              dataKey="x"
              name={xAxisLabel}
              label={{
                value: xAxisLabel,
                position: 'bottom',
                style: {
                  fill: '#0f172a',
                  fontWeight: '800',
                  fontSize: 15,
                  fontFamily: 'Oswald, Impact, sans-serif',
                  letterSpacing: '1px',
                },
              }}
              tick={{ fill: '#1f2937', fontWeight: 700, fontFamily: 'Roboto Condensed, sans-serif' }}
              stroke="#4b5563"
              strokeWidth={2}
              allowDataOverflow={true}
              domain={[left !== null ? left : defaultLeft, right !== null ? right : defaultRight]}
            />
            <YAxis
              type="number"
              dataKey="y"
              name={yAxisLabel}
              label={{
                value: yAxisLabel,
                angle: -90,
                position: 'left',
                style: {
                  fill: '#0f172a',
                  fontWeight: '800',
                  fontSize: 15,
                  fontFamily: 'Oswald, Impact, sans-serif',
                  letterSpacing: '1px',
                },
              }}
              tick={{ fill: '#1f2937', fontWeight: 700, fontFamily: 'Roboto Condensed, sans-serif' }}
              stroke="#4b5563"
              strokeWidth={2}
              allowDataOverflow={true}
              domain={[bottom !== null ? bottom : defaultBottom, top !== null ? top : defaultTop]}
            />
            <Tooltip content={<PlayerTooltip />} cursor={{ strokeDasharray: '3 3' }} />

            {/* Quadrant backgrounds */}
            <ReferenceArea
              x1={defaultLeft}
              x2={xMedian}
              y1={defaultBottom}
              y2={0}
              fill="#ef4444"
              fillOpacity={0.03}
              ifOverflow="visible"
            />
            <ReferenceArea
              x1={xMedian}
              x2={defaultRight}
              y1={defaultBottom}
              y2={0}
              fill="#9ca3af"
              fillOpacity={0.04}
              ifOverflow="visible"
            />
            <ReferenceArea
              x1={defaultLeft}
              x2={xMedian}
              y1={0}
              y2={defaultTop}
              fill="#fbbf24"
              fillOpacity={0.04}
              ifOverflow="visible"
            />
            <ReferenceArea
              x1={xMedian}
              x2={defaultRight}
              y1={0}
              y2={defaultTop}
              fill="#10b981"
              fillOpacity={0.05}
              ifOverflow="visible"
            />

            <ReferenceLine
              x={xMedian}
              stroke="#9ca3af"
              strokeDasharray="5 5"
              strokeWidth={1.5}
              opacity={0.5}
            />
            <ReferenceLine
              y={0}
              stroke="#9ca3af"
              strokeDasharray="5 5"
              strokeWidth={1.5}
              opacity={0.5}
            />

            <Scatter data={chartData} shape={<PlayerHeadshot />} />

            {refAreaLeft && refAreaRight && (
              <ReferenceArea
                x1={refAreaLeft}
                x2={refAreaRight}
                y1={refAreaTop!}
                y2={refAreaBottom!}
                strokeOpacity={0.3}
                fill="#3b82f6"
                fillOpacity={0.3}
              />
            )}
          </ScatterChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
