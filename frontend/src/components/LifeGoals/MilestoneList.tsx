import React, { useState } from 'react';
import type { GoalMilestone, GoalMilestoneCreate, MilestoneStatus } from '../../types/goal';
import { lifeGoalService } from '../../services/lifeGoalService';
import Button from '../common/Button';
import Input from '../common/Input';
import './MilestoneList.css';

interface MilestoneListProps {
  goalId: string;
  milestones: GoalMilestone[];
  onMilestonesChange: (milestones: GoalMilestone[]) => void;
}

const MilestoneList: React.FC<MilestoneListProps> = ({
  goalId,
  milestones,
  onMilestonesChange,
}) => {
  const [showForm, setShowForm] = useState(false);
  const [newMilestone, setNewMilestone] = useState<GoalMilestoneCreate>({
    title: '',
    description: '',
    order_index: milestones.length,
  });

  const handleAddMilestone = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!newMilestone.title.trim()) return;

    try {
      const created = await lifeGoalService.createMilestone(goalId, newMilestone);
      onMilestonesChange([...milestones, created]);
      setNewMilestone({ title: '', description: '', order_index: milestones.length + 1 });
      setShowForm(false);
    } catch (err) {
      console.error('Failed to create milestone:', err);
    }
  };

  const handleUpdateStatus = async (milestoneId: string, status: MilestoneStatus) => {
    try {
      const updated = await lifeGoalService.updateMilestone(goalId, milestoneId, { status });
      onMilestonesChange(
        milestones.map(m => (m.id === milestoneId ? updated : m))
      );
    } catch (err) {
      console.error('Failed to update milestone:', err);
    }
  };

  const handleDeleteMilestone = async (milestoneId: string) => {
    if (!window.confirm('Are you sure you want to delete this milestone?')) {
      return;
    }

    try {
      await lifeGoalService.deleteMilestone(goalId, milestoneId);
      onMilestonesChange(milestones.filter(m => m.id !== milestoneId));
    } catch (err) {
      console.error('Failed to delete milestone:', err);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return '✓';
      case 'in_progress':
        return '⟳';
      case 'pending':
        return '○';
      case 'skipped':
        return '⊘';
      default:
        return '○';
    }
  };

  const sortedMilestones = [...milestones].sort((a, b) => a.order_index - b.order_index);

  return (
    <div className="milestone-list">
      <div className="milestone-header">
        <h4>Milestones ({milestones.length})</h4>
        <Button onClick={() => setShowForm(!showForm)} variant="secondary">
          {showForm ? 'Cancel' : '+ Add Milestone'}
        </Button>
      </div>

      {showForm && (
        <form onSubmit={handleAddMilestone} className="milestone-form">
          <Input
            label="Milestone Title"
            value={newMilestone.title}
            onChange={(e) =>
              setNewMilestone(prev => ({ ...prev, title: e.target.value }))
            }
            placeholder="e.g., Research potential neighborhoods"
            required
          />
          <Input
            label="Description (Optional)"
            value={newMilestone.description || ''}
            onChange={(e) =>
              setNewMilestone(prev => ({ ...prev, description: e.target.value }))
            }
            placeholder="Additional details..."
          />
          <Button type="submit" variant="primary">
            Add Milestone
          </Button>
        </form>
      )}

      {sortedMilestones.length === 0 ? (
        <div className="milestones-empty">
          <p>No milestones yet. Add milestones to track progress step by step.</p>
        </div>
      ) : (
        <div className="milestones-container">
          {sortedMilestones.map((milestone, index) => (
            <div key={milestone.id} className={`milestone-item status-${milestone.status}`}>
              <div className="milestone-number">{index + 1}</div>
              <div className="milestone-content">
                <div className="milestone-title-row">
                  <span className="milestone-icon">{getStatusIcon(milestone.status)}</span>
                  <h5>{milestone.title}</h5>
                </div>
                {milestone.description && (
                  <p className="milestone-description">{milestone.description}</p>
                )}
                {milestone.target_date && (
                  <span className="milestone-date">
                    Target: {new Date(milestone.target_date).toLocaleDateString()}
                  </span>
                )}
              </div>
              <div className="milestone-actions">
                <select
                  value={milestone.status}
                  onChange={(e) =>
                    handleUpdateStatus(milestone.id, e.target.value as MilestoneStatus)
                  }
                  className="milestone-status-select"
                >
                  <option value="pending">Pending</option>
                  <option value="in_progress">In Progress</option>
                  <option value="completed">Completed</option>
                  <option value="skipped">Skipped</option>
                </select>
                <button
                  onClick={() => handleDeleteMilestone(milestone.id)}
                  className="milestone-delete"
                  aria-label="Delete milestone"
                >
                  ×
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MilestoneList;
