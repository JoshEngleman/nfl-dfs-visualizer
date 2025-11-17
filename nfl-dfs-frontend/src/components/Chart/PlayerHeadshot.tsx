import type { ChartData } from '../../types/player';

interface PlayerHeadshotProps {
  cx?: number;
  cy?: number;
  payload?: ChartData & {
    color: string;
    intensity: number;
    rawSize: number;
    player_id: string;
  };
  index?: number;
}

// These will be calculated by parent component
let minSize = 0;
let maxSize = 100;
let x75th = 0;
let y75th = 0;
let chartData: any[] = [];

export function setHeadshotContext(data: {
  minSize: number;
  maxSize: number;
  x75th: number;
  y75th: number;
  chartData: any[];
}) {
  minSize = data.minSize;
  maxSize = data.maxSize;
  x75th = data.x75th;
  y75th = data.y75th;
  chartData = data.chartData;
}

export default function PlayerHeadshot(props: PlayerHeadshotProps) {
  const { cx = 0, cy = 0, payload, index = 0 } = props;

  if (!payload) return null;

  // Calculate size based on z value
  const sizeNormalized = (payload.rawSize - minSize) / (maxSize - minSize || 1);
  const size = 24 + sizeNormalized * 24;
  const radius = size / 2;

  const borderOpacity = payload.intensity;
  const glowOpacity = payload.intensity * 0.3;

  // Extract last name
  const nameParts = payload.player_name.split(' ');
  let lastName = payload.player_name;
  if (nameParts.length > 1) {
    const lastPart = nameParts[nameParts.length - 1];
    const suffixes = ['Jr.', 'Sr.', 'II', 'III', 'IV', 'V'];
    if (suffixes.includes(lastPart) && nameParts.length > 2) {
      lastName = nameParts[nameParts.length - 2];
    } else {
      lastName = lastPart;
    }
  }

  // Only show labels for top performers (above 75th percentile in either axis)
  const showLabel = payload.x >= x75th || payload.y >= y75th;

  // Smart label positioning to avoid overlaps
  const nearbyPlayers = chartData.filter((other, idx) => {
    if (idx === index) return false;
    const distance = Math.sqrt(Math.pow(other.x - payload.x, 2) + Math.pow(other.y - payload.y, 2));
    return distance < 3; // Within 3 units
  });

  // Default position: below
  let labelX = cx;
  let labelY = cy + radius + 12;
  let labelAnchor: 'start' | 'middle' | 'end' = 'middle';

  // If crowded, use hash-based positioning
  if (nearbyPlayers.length > 0) {
    const hash =
      payload.player_id.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0) % 4;
    if (hash === 0) {
      // Below-right
      labelX = cx + radius + 5;
      labelY = cy + radius + 8;
      labelAnchor = 'start';
    } else if (hash === 1) {
      // Below-left
      labelX = cx - radius - 5;
      labelY = cy + radius + 8;
      labelAnchor = 'end';
    } else if (hash === 2) {
      // Above
      labelY = cy - radius - 4;
    } else {
      // Below with extra offset
      labelY = cy + radius + 18;
    }
  }

  // Team logo watermark
  const teamLogoUrl = `https://a.espncdn.com/i/teamlogos/nfl/500/${payload.team_abbr.toUpperCase()}.png`;
  const watermarkSize = size * 1.3;

  return (
    <g>
      {/* Glow effect */}
      <circle cx={cx} cy={cy} r={radius + 2} fill={payload.color} opacity={glowOpacity} />

      {/* Clip paths */}
      <defs>
        <clipPath id={`clip-${payload.player_id}`}>
          <circle cx={cx} cy={cy} r={radius} />
        </clipPath>
        <clipPath id={`clip-watermark-${payload.player_id}`}>
          <circle cx={cx} cy={cy} r={radius} />
        </clipPath>
      </defs>

      {/* White background */}
      <circle cx={cx} cy={cy} r={radius} fill="white" />

      {/* Team logo watermark */}
      <image
        x={cx - watermarkSize / 2}
        y={cy - watermarkSize / 2}
        width={watermarkSize}
        height={watermarkSize}
        href={teamLogoUrl}
        clipPath={`url(#clip-watermark-${payload.player_id})`}
        opacity={0.18}
        preserveAspectRatio="xMidYMid meet"
      />

      {/* Player headshot */}
      <image
        x={cx - radius}
        y={cy - radius}
        width={size}
        height={size}
        href={payload.headshot_url}
        clipPath={`url(#clip-${payload.player_id})`}
        preserveAspectRatio="xMidYMid slice"
        opacity={0.9}
      />

      {/* Border */}
      <circle
        cx={cx}
        cy={cy}
        r={radius}
        fill="none"
        stroke={payload.color}
        strokeWidth={2.5}
        opacity={borderOpacity}
      />

      {/* Label for top performers */}
      {showLabel && (
        <>
          {/* White outline */}
          <text
            x={labelX}
            y={labelY}
            textAnchor={labelAnchor}
            fill="white"
            fontSize="10"
            fontWeight="700"
            opacity={0.8}
            stroke="white"
            strokeWidth="4"
            style={{
              pointerEvents: 'none',
              fontFamily: 'Roboto Condensed, Arial Narrow, sans-serif',
              letterSpacing: '0.5px',
            }}
          >
            {lastName.toUpperCase()}
          </text>
          {/* Black text */}
          <text
            x={labelX}
            y={labelY}
            textAnchor={labelAnchor}
            fill="#0f172a"
            fontSize="10"
            fontWeight="700"
            opacity={1}
            style={{
              pointerEvents: 'none',
              fontFamily: 'Roboto Condensed, Arial Narrow, sans-serif',
              letterSpacing: '0.5px',
            }}
          >
            {lastName.toUpperCase()}
          </text>
        </>
      )}
    </g>
  );
}
