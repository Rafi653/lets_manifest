import React from 'react';
import { Outlet } from 'react-router-dom';
import Header from '../Header';
import './MainLayout.css';

const MainLayout: React.FC = () => {
  return (
    <div className="main-layout">
      <Header />
      <main className="main-content">
        <Outlet />
      </main>
      <footer className="footer">
        <p>&copy; 2025 Let's Manifest. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default MainLayout;
