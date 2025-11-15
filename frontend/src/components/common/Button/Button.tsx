/**
 * Reusable Button component with different variants
 */

import React from 'react';
import './Button.css';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'success';
  fullWidth?: boolean;
  loading?: boolean;
}

const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  fullWidth = false,
  loading = false,
  className = '',
  disabled,
  ...rest
}) => {
  return (
    <button
      className={`btn btn-${variant} ${fullWidth ? 'btn-full-width' : ''} ${className}`}
      disabled={disabled || loading}
      aria-busy={loading}
      {...rest}
    >
      {loading ? (
        <span className="btn-loading">
          <span className="spinner" aria-hidden="true"></span>
          Loading...
        </span>
      ) : (
        children
      )}
    </button>
  );
};

export default Button;
