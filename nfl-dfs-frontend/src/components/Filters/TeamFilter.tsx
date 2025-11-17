import React from 'react';
import { getTeamLogoUrl } from '../../utils/teamColors';
import './TeamFilter.css';
import './Filters.css';

interface TeamFilterProps {
  allTeams: string[];
  selectedTeams: string[];
  onToggleTeam: (team: string) => void;
}

const TeamFilter: React.FC<TeamFilterProps> = ({
  allTeams,
  selectedTeams,
  onToggleTeam
}) => {
  const halfwayIndex = Math.ceil(allTeams.length / 2);
  const firstHalf = allTeams.slice(0, halfwayIndex);
  const secondHalf = allTeams.slice(halfwayIndex);

  return (
    <div className="filter-group">
      <div className="filter-group-header">Teams</div>
      <div className="filter-group-content">
        <div className="team-logos-container">
          {/* First Row - Half of teams */}
          <div className="team-logos-row">
            {firstHalf.map(team => (
              <img
                key={team}
                src={getTeamLogoUrl(team)}
                alt={team}
                title={team}
                className={`team-logo-toggle ${
                  selectedTeams.includes(team) ? 'active' : 'inactive'
                }`}
                onClick={() => onToggleTeam(team)}
              />
            ))}
          </div>
          {/* Second Row - Other half of teams */}
          <div className="team-logos-row">
            {secondHalf.map(team => (
              <img
                key={team}
                src={getTeamLogoUrl(team)}
                alt={team}
                title={team}
                className={`team-logo-toggle ${
                  selectedTeams.includes(team) ? 'active' : 'inactive'
                }`}
                onClick={() => onToggleTeam(team)}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TeamFilter;
