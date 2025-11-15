import React from 'react';
import './Dashboard.css';

const Dashboard: React.FC = () => {
  return (
    <div className="page-container">
      <h1>Dashboard</h1>
      <p>Welcome to Let's Manifest! Track your goals, habits, and progress all in one place.</p>
      <div className="dashboard-grid">
        <div className="dashboard-card">
          <h3>Goals</h3>
          <p>Track your manifestation goals</p>
        </div>
        <div className="dashboard-card">
          <h3>Habits</h3>
          <p>Build positive daily habits</p>
        </div>
        <div className="dashboard-card">
          <h3>Food</h3>
          <p>Monitor your nutrition</p>
        </div>
        <div className="dashboard-card">
          <h3>Workouts</h3>
          <p>Track your fitness journey</p>
        </div>
        <div className="dashboard-card">
          <h3>Review</h3>
          <p>Daily reflections and reviews</p>
        </div>
        <div className="dashboard-card">
          <h3>Progress</h3>
          <p>View your overall progress</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
