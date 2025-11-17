import type { ChartData } from '../../types/player';
import './PlayerTooltip.css';

interface PlayerTooltipProps {
  active?: boolean;
  payload?: Array<{ payload: ChartData }>;
}

export default function PlayerTooltip({ active, payload }: PlayerTooltipProps) {
  if (!active || !payload || !payload.length) {
    return null;
  }

  const data = payload[0].payload;

  // Format salary
  const formatSalary = (salary: number) => {
    return `$${(salary / 1000).toFixed(1)}K`;
  };

  // Format percentage
  const formatPct = (value: number) => {
    return `${value.toFixed(1)}%`;
  };

  // Format leverage with color
  const formatLeverage = (value: number) => {
    const formatted = value.toFixed(2);
    const className =
      value >= 0 ? 'player-card-leverage-positive' : 'player-card-leverage-negative';
    return (
      <span className={className}>
        {value >= 0 ? '+' : ''}
        {formatted}
      </span>
    );
  };

  const placeholderImage =
    'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHZpZXdCb3g9IjAgMCA2NCA2NCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIGZpbGw9IiNlNWU3ZWIiLz48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjI0IiBmaWxsPSIjOWNhM2FmIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkeT0iLjNlbSI+Pz88L3RleHQ+PC9zdmc+';

  return (
    <div className="player-card-tooltip">
      {/* Header with headshot, name, position, team, salary */}
      <div className="player-card-header">
        <img
          src={data.headshot_url || placeholderImage}
          alt={data.player_name}
          className="player-card-headshot"
          loading="lazy"
          onError={(e) => {
            e.currentTarget.src = placeholderImage;
          }}
        />
        <div className="player-card-info">
          <div className="player-card-name">{data.player_name}</div>
          <div className="player-card-meta">
            <span className={`player-card-position-badge ${data.position}`}>{data.position}</span>
            <span>•</span>
            <span>{data.team_abbr}</span>
            <span>•</span>
            <span>{formatSalary(data.salary)}</span>
          </div>
        </div>
      </div>

      {/* Projections Section */}
      <div className="player-card-section">
        <div className="player-card-section-title">Projections</div>
        <div className="player-card-stats">
          <div className="player-card-stat player-card-stat-primary">
            <span className="player-card-stat-label">Proj:</span>
            <span className="player-card-stat-value">{data.projection.toFixed(1)} pts</span>
          </div>
          <div className="player-card-stat">
            <span className="player-card-stat-label">Pts/$:</span>
            <span className="player-card-stat-value">{data.pts_per_dollar.toFixed(3)}</span>
          </div>
        </div>
      </div>

      {/* Performance Section */}
      <div className="player-card-section">
        <div className="player-card-section-title">Performance</div>
        <div className="player-card-stats">
          <div className="player-card-stat">
            <span className="player-card-stat-label">Boom:</span>
            <span className="player-card-stat-value">{formatPct(data.boom_pct)}</span>
          </div>
        </div>
      </div>

      {/* Ownership & Value Section */}
      <div className="player-card-section">
        <div className="player-card-section-title">Ownership & Value</div>
        <div className="player-card-stats">
          <div className="player-card-stat">
            <span className="player-card-stat-label">Own:</span>
            <span className="player-card-stat-value">{formatPct(data.proj_ownership)}</span>
          </div>
          <div className="player-card-stat">
            <span className="player-card-stat-label">Leverage:</span>
            <span className="player-card-stat-value">{formatLeverage(data.leverage)}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
