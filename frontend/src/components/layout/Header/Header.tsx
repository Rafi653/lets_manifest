import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Header.css';

const Header: React.FC = () => {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Dashboard', icon: '🏠' },
    { path: '/goals', label: 'Goals', icon: '🎯' },
    { path: '/habits', label: 'Habits', icon: '✅' },
    { path: '/food', label: 'Food', icon: '🍎' },
    { path: '/workouts', label: 'Workouts', icon: '💪' },
    { path: '/review', label: 'Review', icon: '📝' },
    { path: '/blog', label: 'Blog', icon: '✍️' },
    { path: '/progress', label: 'Progress', icon: '📊' },
  ];

  return (
    <header className="header">
      <div className="header-content">
        <div className="logo">
          <h1>✨ Let's Manifest</h1>
        </div>
        <nav className="nav">
          <ul className="nav-list">
            {navItems.map((item) => (
              <li key={item.path} className="nav-item">
                <Link
                  to={item.path}
                  className={`nav-link ${location.pathname === item.path ? 'active' : ''}`}
                >
                  <span className="nav-icon">{item.icon}</span>
                  <span className="nav-label">{item.label}</span>
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;
