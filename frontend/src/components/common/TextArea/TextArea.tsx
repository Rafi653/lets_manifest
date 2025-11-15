/**
 * Reusable TextArea component with label and validation support
 */

import React from 'react';
import './TextArea.css';

interface TextAreaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label: string;
  error?: string;
  helperText?: string;
}

const TextArea: React.FC<TextAreaProps> = ({
  label,
  error,
  helperText,
  id,
  className = '',
  ...rest
}) => {
  const textAreaId = id || label.toLowerCase().replace(/\s+/g, '-');

  return (
    <div className={`textarea-wrapper ${className}`}>
      <label htmlFor={textAreaId} className="textarea-label">
        {label}
        {rest.required && <span className="required-indicator" aria-label="required">*</span>}
      </label>
      <textarea
        id={textAreaId}
        className={`textarea-field ${error ? 'textarea-error' : ''}`}
        aria-invalid={error ? 'true' : 'false'}
        aria-describedby={error ? `${textAreaId}-error` : helperText ? `${textAreaId}-helper` : undefined}
        rows={4}
        {...rest}
      />
      {error && (
        <span id={`${textAreaId}-error`} className="error-message" role="alert">
          {error}
        </span>
      )}
      {!error && helperText && (
        <span id={`${textAreaId}-helper`} className="helper-text">
          {helperText}
        </span>
      )}
    </div>
  );
};

export default TextArea;
