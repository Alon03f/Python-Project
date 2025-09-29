import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import api from '../services/api';
import { PenSquare } from 'lucide-react';
import toast from 'react-hot-toast';
import './ArticleForm.css';

const CreateArticle = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        title: '',
        content: '',
        excerpt: '',
        tags: '',
        is_published: true,
    });

    const createMutation = useMutation({
        mutationFn: async (data) => {
            const tagsArray = data.tags
                .split(',')
                .map((tag) => tag.trim())
                .filter((tag) => tag);

            const response = await api.post('/api/articles/', {
                ...data,
                tags: tagsArray,
            });
            return response.data;
        },
        onSuccess: (data) => {
            toast.success('Article created successfully!');
            navigate(`/articles/${data.slug}`);
        },
        onError: (error) => {
            toast.error(error.response?.data?.message || 'Failed to create article');
        },
    });

    const handleChange = (e) => {
        const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
        setFormData({
            ...formData,
            [e.target.name]: value,
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        createMutation.mutate(formData);
    };

    return (
        <div className="article-form-container">
            <div className="article-form-card">
                <div className="form-header">
                    <PenSquare size={32} />
                    <h1>Create New Article</h1>
                </div>

                <form onSubmit={handleSubmit} className="article-form">
                    <div className="form-group">
                        <label htmlFor="title">Title *</label>
                        <input
                            type="text"
                            id="title"
                            name="title"
                            value={formData.title}
                            onChange={handleChange}
                            className="form-control"
                            required
                            placeholder="Enter article title..."
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="excerpt">Excerpt</label>
                        <textarea
                            id="excerpt"
                            name="excerpt"
                            value={formData.excerpt}
                            onChange={handleChange}
                            className="form-control"
                            rows="3"
                            placeholder="Short summary of your article (optional)..."
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="content">Content *</label>
                        <textarea
                            id="content"
                            name="content"
                            value={formData.content}
                            onChange={handleChange}
                            className="form-control"
                            rows="15"
                            required
                            placeholder="Write your article content here..."
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="tags">Tags</label>
                        <input
                            type="text"
                            id="tags"
                            name="tags"
                            value={formData.tags}
                            onChange={handleChange}
                            className="form-control"
                            placeholder="Enter tags separated by commas (e.g. python, django, web)"
                        />
                        <small className="form-text">Separate tags with commas. Maximum 10 tags.</small>
                    </div>

                    <div className="form-group-checkbox">
                        <input
                            type="checkbox"
                            id="is_published"
                            name="is_published"
                            checked={formData.is_published}
                            onChange={handleChange}
                        />
                        <label htmlFor="is_published">Publish article immediately</label>
                    </div>

                    <div className="form-actions">
                        <button
                            type="submit"
                            className="btn btn-success"
                            disabled={createMutation.isPending}
                        >
                            {createMutation.isPending ? 'Creating...' : 'Create Article'}
                        </button>
                        <button
                            type="button"
                            onClick={() => navigate(-1)}
                            className="btn btn-secondary"
                        >
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default CreateArticle;