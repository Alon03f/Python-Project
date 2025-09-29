import React from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '../services/api';
import ArticleCard from '../components/ArticleCard';
import { BookMarked } from 'lucide-react';
import './Bookmarks.css';

const Bookmarks = () => {
    const { data: bookmarks, isLoading } = useQuery({
        queryKey: ['bookmarks'],
        queryFn: async () => {
            const response = await api.get('/api/bookmarks/');
            return response.data;
        },
    });

    if (isLoading) {
        return (
            <div className="loading">
                <div className="spinner"></div>
            </div>
        );
    }

    return (
        <div className="bookmarks-page">
            <div className="page-header">
                <BookMarked size={32} />
                <h1>My Bookmarks</h1>
                <p>Articles you've saved for later</p>
            </div>

            {bookmarks?.length === 0 ? (
                <div className="no-results">
                    <BookMarked size={64} />
                    <h2>No bookmarks yet</h2>
                    <p>Start bookmarking articles to save them for later!</p>
                </div>
            ) : (
                <div className="articles-grid">
                    {bookmarks?.map((bookmark) => (
                        <ArticleCard key={bookmark.id} article={bookmark.article} />
                    ))}
                </div>
            )}
        </div>
    );
};

export default Bookmarks;