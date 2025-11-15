/**
 * BlogEntryForm component for creating and editing blog entries
 */

import React, { useState } from 'react';
import type { BlogEntry, BlogEntryCreate, BlogEntryUpdate } from '../../types/blogEntry';
import Input from '../common/Input';
import TextArea from '../common/TextArea';
import Button from '../common/Button';
import './BlogEntryForm.css';

interface BlogEntryFormProps {
  entry?: BlogEntry;
  onSubmit: (data: BlogEntryCreate | BlogEntryUpdate) => Promise<void>;
  onCancel: () => void;
}

const BlogEntryForm: React.FC<BlogEntryFormProps> = ({ entry, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    title: entry?.title || '',
    content: entry?.content || '',
    excerpt: entry?.excerpt || '',
    status: entry?.status || 'draft',
    is_public: entry?.is_public || false,
    is_featured: entry?.is_featured || false,
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value, type } = e.target;
    const newValue = type === 'checkbox' ? (e.target as HTMLInputElement).checked : value;
    
    setFormData((prev) => ({ ...prev, [name]: newValue }));
    
    // Clear error for this field
    if (errors[name]) {
      setErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    } else if (formData.title.length > 500) {
      newErrors.title = 'Title must be 500 characters or less';
    }

    if (!formData.content.trim()) {
      newErrors.content = 'Content is required';
    }

    if (!['draft', 'published', 'archived'].includes(formData.status)) {
      newErrors.status = 'Invalid status';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) {
      return;
    }

    setLoading(true);

    try {
      const submitData: BlogEntryCreate | BlogEntryUpdate = {
        title: formData.title.trim(),
        content: formData.content.trim(),
        excerpt: formData.excerpt.trim() || undefined,
        status: formData.status as 'draft' | 'published' | 'archived',
        is_public: formData.is_public,
        is_featured: formData.is_featured,
      };

      await onSubmit(submitData);
    } catch (error) {
      console.error('Form submission error:', error);
      setErrors({ submit: 'Failed to save blog entry. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="blog-entry-form" onSubmit={handleSubmit}>
      <div className="form-section">
        <Input
          label="Title"
          name="title"
          type="text"
          value={formData.title}
          onChange={handleChange}
          error={errors.title}
          required
          placeholder="Enter a compelling title..."
        />

        <TextArea
          label="Excerpt (Optional)"
          name="excerpt"
          value={formData.excerpt}
          onChange={handleChange}
          error={errors.excerpt}
          placeholder="Brief summary or preview of your post..."
          rows={2}
        />

        <TextArea
          label="Content"
          name="content"
          value={formData.content}
          onChange={handleChange}
          error={errors.content}
          placeholder="Share your thoughts, experiences, and reflections..."
          rows={15}
          required
        />
      </div>

      <div className="form-section">
        <h3 className="section-title">Publication Settings</h3>

        <div className="form-row">
          <div className="form-field">
            <label htmlFor="status" className="form-label">Status</label>
            <select
              id="status"
              name="status"
              value={formData.status}
              onChange={handleChange}
              className="form-select"
            >
              <option value="draft">Draft</option>
              <option value="published">Published</option>
              <option value="archived">Archived</option>
            </select>
            {errors.status && <span className="error-text">{errors.status}</span>}
          </div>
        </div>

        <div className="form-checkboxes">
          <label className="checkbox-label">
            <input
              type="checkbox"
              name="is_public"
              checked={formData.is_public}
              onChange={handleChange}
            />
            <span>Make this post public</span>
          </label>

          <label className="checkbox-label">
            <input
              type="checkbox"
              name="is_featured"
              checked={formData.is_featured}
              onChange={handleChange}
            />
            <span>Feature this post</span>
          </label>
        </div>
      </div>

      {errors.submit && (
        <div className="form-error" role="alert">
          {errors.submit}
        </div>
      )}

      <div className="form-actions">
        <Button type="button" variant="secondary" onClick={onCancel}>
          Cancel
        </Button>
        <Button type="submit" variant="primary" loading={loading}>
          {entry ? 'Update Entry' : 'Create Entry'}
        </Button>
      </div>
    </form>
  );
};

export default BlogEntryForm;
