/**
 * Reusable Input component with label and validation support
 */

import React from 'react';
import './Input.css';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
  helperText?: string;
}

const Input: React.FC<InputProps> = ({
  label,
  error,
  helperText,
  id,
  className = '',
  ...rest
}) => {
  const inputId = id || label.toLowerCase().replace(/\s+/g, '-');

  return (
    <div className={`input-wrapper ${className}`}>
      <label htmlFor={inputId} className="input-label">
        {label}
        {rest.required && <span className="required-indicator" aria-label="required">*</span>}
      </label>
      <input
        id={inputId}
        className={`input-field ${error ? 'input-error' : ''}`}
        aria-invalid={error ? 'true' : 'false'}
        aria-describedby={error ? `${inputId}-error` : helperText ? `${inputId}-helper` : undefined}
        {...rest}
      />
      {error && (
        <span id={`${inputId}-error`} className="error-message" role="alert">
          {error}
        </span>
      )}
      {!error && helperText && (
        <span id={`${inputId}-helper`} className="helper-text">
          {helperText}
        </span>
      )}
    </div>
  );
};

export default Input;
