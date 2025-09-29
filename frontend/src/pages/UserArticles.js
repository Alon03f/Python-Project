import React from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import api from '../services/api';
import ArticleCard from '../components/ArticleCard';
import { User } from 'lucide-react';
import './UserArticles.css';

const UserArticles = () => {
    const { userId } = useParams();

    const { data: user, isLoading: userLoading } = useQuery({
        queryKey: ['user', userId],
        queryFn: async () => {
            const response = await api.get(`/api/users/${userId}/`);
            return response.data;
        },
    });

    const { data: articles, isLoading: articlesLoading } = useQuery({
        queryKey: ['user-articles', userId],
        queryFn: async () => {
            const response = await api.get(`/api/users/${userId}/articles/`);
            return response.data;
        },
    });

    if (userLoading || articlesLoading) {
        return (
            <div className="loading">
                <div className="spinner"></div>
            </div>
        );
    }

    return (
        <div className="user-articles-page">
            <div className="user-header">
                <div className="user-avatar">
                    <User size={48} />
                </div>
                <h1>{user?.username}'s Articles</h1>
                <p>
                    {user?.first_name} {user?.last_name}
                </p>
                <div className="user-stats">
                    <span>{user?.articles_count} articles</span>
                    <span>•</span>
                    <span>{user?.comments_count} comments</span>
                </div>
            </div>

            <div className="articles-grid">
                {articles?.map((article) => (
                    <ArticleCard key={article.id} article={article} />
                ))}
            </div>

            {articles?.length === 0 && (
                <div className="no-results">
                    <p>This user hasn't published any articles yet</p>
                </div>
            )}
        </div>
    );
};

export default UserArticles;