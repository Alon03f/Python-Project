import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../services/api';
import { Edit } from 'lucide-react';
import toast from 'react-hot-toast';
import './ArticleForm.css';

const EditArticle = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const queryClient = useQueryClient();
    const [formData, setFormData] = useState({
        title: '',
        content: '',
        excerpt: '',
        tags: '',
        is_published: true,
    });

    const { data: article, isLoading } = useQuery({
        queryKey: ['article-edit', id],
        queryFn: async () => {
            const response = await api.get(`/api/articles/${id}/`);
            return response.data;
        },
    });

    useEffect(() => {
        if (article) {
            setFormData({
                title: article.title,
                content: article.content,
                excerpt: article.excerpt || '',
                tags: article.tags?.map((tag) => tag.name).join(', ') || '',
                is_published: article.is_published,
            });
        }
    }, [article]);

    const updateMutation = useMutation({
        mutationFn: async (data) => {
            const tagsArray = data.tags
                .split(',')
                .map((tag) => tag.trim())
                .filter((tag) => tag);

            const response = await api.patch(`/api/articles/${id}/`, {
                ...data,
                tags: tagsArray,
            });
            return response.data;
        },
        onSuccess: () => {
            toast.success('Article updated successfully!');
            queryClient.invalidateQueries(['article', article.slug]);
            navigate(`/articles/${article.slug}`);
        },
        onError: (error) => {
            toast.error(error.response?.data?.message || 'Failed to update article');
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
        updateMutation.mutate(formData);
    };

    if (isLoading) {
        return (
            <div className="loading">
                <div className="spinner"></div>
            </div>
        );
    }

    return (
        <div className="article-form-container">
            <div className="article-form-card">
                <div className="form-header">
                    <Edit size={32} />
                    <h1>Edit Article</h1>
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
                        <label htmlFor="is_published">Published</label>
                    </div>

                    <div className="form-actions">
                        <button
                            type="submit"
                            className="btn btn-success"
                            disabled={updateMutation.isPending}
                        >
                            {updateMutation.isPending ? 'Updating...' : 'Update Article'}
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

export default EditArticle;