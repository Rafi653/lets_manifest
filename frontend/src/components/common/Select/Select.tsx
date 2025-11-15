/**
 * Reusable Select component with label and validation support
 */

import React from 'react';
import './Select.css';

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label: string;
  error?: string;
  helperText?: string;
  options: { value: string; label: string }[];
}

const Select: React.FC<SelectProps> = ({
  label,
  error,
  helperText,
  options,
  id,
  className = '',
  ...rest
}) => {
  const selectId = id || label.toLowerCase().replace(/\s+/g, '-');

  return (
    <div className={`select-wrapper ${className}`}>
      <label htmlFor={selectId} className="select-label">
        {label}
        {rest.required && <span className="required-indicator" aria-label="required">*</span>}
      </label>
      <select
        id={selectId}
        className={`select-field ${error ? 'select-error' : ''}`}
        aria-invalid={error ? 'true' : 'false'}
        aria-describedby={error ? `${selectId}-error` : helperText ? `${selectId}-helper` : undefined}
        {...rest}
      >
        <option value="">Select an option</option>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {error && (
        <span id={`${selectId}-error`} className="error-message" role="alert">
          {error}
        </span>
      )}
      {!error && helperText && (
        <span id={`${selectId}-helper`} className="helper-text">
          {helperText}
        </span>
      )}
    </div>
  );
};

export default Select;
