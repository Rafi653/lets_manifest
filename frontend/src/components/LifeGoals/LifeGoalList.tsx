import React, { useState } from 'react';
import type { Goal, GoalMilestone } from '../../types/goal';
import { lifeGoalService } from '../../services/lifeGoalService';
import Button from '../common/Button';
import MilestoneList from './MilestoneList';
import './LifeGoalList.css';

interface LifeGoalListProps {
  goals: Goal[];
  onEdit: (goal: Goal) => void;
  onDelete: (goalId: string) => void;
  loading: boolean;
}

const LifeGoalList: React.FC<LifeGoalListProps> = ({ goals, onEdit, onDelete, loading }) => {
  const [expandedGoalId, setExpandedGoalId] = useState<string | null>(null);
  const [milestones, setMilestones] = useState<Record<string, GoalMilestone[]>>({});

  const handleToggleExpand = async (goalId: string) => {
    if (expandedGoalId === goalId) {
      setExpandedGoalId(null);
      return;
    }

    setExpandedGoalId(goalId);

    // Load milestones if not already loaded
    if (!milestones[goalId]) {
      try {
        const goalMilestones = await lifeGoalService.getMilestones(goalId);
        setMilestones(prev => ({ ...prev, [goalId]: goalMilestones }));
      } catch (err) {
        console.error('Failed to load milestones:', err);
      }
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'status-completed';
      case 'in_progress':
        return 'status-in-progress';
      case 'active':
        return 'status-active';
      case 'paused':
        return 'status-paused';
      case 'cancelled':
        return 'status-cancelled';
      default:
        return 'status-active';
    }
  };

  const getPriorityLabel = (priority: number) => {
    if (priority >= 5) return 'High';
    if (priority >= 4) return 'Medium-High';
    if (priority >= 3) return 'Medium';
    if (priority >= 2) return 'Medium-Low';
    return 'Low';
  };

  const formatLifeArea = (area: string | null) => {
    if (!area) return 'Uncategorized';
    return area.charAt(0).toUpperCase() + area.slice(1).replace('_', ' ');
  };

  if (loading) {
    return (
      <div className="life-goal-list loading">
        <p>Loading life goals...</p>
      </div>
    );
  }

  if (goals.length === 0) {
    return (
      <div className="life-goal-list empty">
        <div className="empty-state">
          <h3>No Life Goals Yet</h3>
          <p>Start tracking your long-term aspirations by creating your first life goal.</p>
        </div>
      </div>
    );
  }

  // Group goals by life area
  const groupedGoals = goals.reduce((acc, goal) => {
    const area = goal.category || 'uncategorized';
    if (!acc[area]) {
      acc[area] = [];
    }
    acc[area].push(goal);
    return acc;
  }, {} as Record<string, Goal[]>);

  return (
    <div className="life-goal-list">
      {Object.entries(groupedGoals).map(([area, areaGoals]) => (
        <div key={area} className="life-area-section">
          <h3 className="life-area-title">{formatLifeArea(area)}</h3>
          <div className="goals-grid">
            {areaGoals.map(goal => (
              <div key={goal.id} className="life-goal-card">
                <div className="goal-header">
                  <div className="goal-title-row">
                    <h4>{goal.title}</h4>
                    <span className={`goal-status ${getStatusColor(goal.status)}`}>
                      {goal.status.replace('_', ' ')}
                    </span>
                  </div>
                  <div className="goal-meta">
                    <span className="goal-priority">Priority: {getPriorityLabel(goal.priority)}</span>
                    {goal.target_value && goal.target_unit && (
                      <span className="goal-target">
                        Target: {goal.target_value} {goal.target_unit}
                      </span>
                    )}
                  </div>
                </div>

                {goal.description && (
                  <p className="goal-description">{goal.description}</p>
                )}

                {goal.target_value && (
                  <div className="goal-progress">
                    <div className="progress-bar">
                      <div
                        className="progress-fill"
                        style={{
                          width: `${Math.min(
                            100,
                            (Number(goal.current_value) / Number(goal.target_value)) * 100
                          )}%`,
                        }}
                      />
                    </div>
                    <div className="progress-label">
                      {goal.current_value} / {goal.target_value} {goal.target_unit}
                    </div>
                  </div>
                )}

                <div className="goal-actions">
                  <Button onClick={() => handleToggleExpand(goal.id)} variant="secondary" size="small">
                    {expandedGoalId === goal.id ? 'Hide' : 'Show'} Milestones
                  </Button>
                  <Button onClick={() => onEdit(goal)} variant="secondary" size="small">
                    Edit
                  </Button>
                  <Button onClick={() => onDelete(goal.id)} variant="danger" size="small">
                    Delete
                  </Button>
                </div>

                {expandedGoalId === goal.id && (
                  <div className="goal-milestones">
                    <MilestoneList
                      goalId={goal.id}
                      milestones={milestones[goal.id] || []}
                      onMilestonesChange={(updated) => 
                        setMilestones(prev => ({ ...prev, [goal.id]: updated }))
                      }
                    />
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default LifeGoalList;
