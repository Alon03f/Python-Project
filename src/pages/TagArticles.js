import React from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import api from '../services/api';
import ArticleCard from '../components/ArticleCard';
import { Tag } from 'lucide-react';
import './TagArticles.css';

const TagArticles = () => {
    const { slug } = useParams();

    const { data: tag, isLoading: tagLoading } = useQuery({
        queryKey: ['tag', slug],
        queryFn: async () => {
            const response = await api.get(`/api/tags/`);
            const tags = response.data.results || response.data;
            return tags.find((t) => t.slug === slug);
        },
    });

    const { data: articles, isLoading: articlesLoading } = useQuery({
        queryKey: ['tag-articles', tag?.id],
        queryFn: async () => {
            const response = await api.get(`/api/tags/${tag.id}/articles/`);
            return response.data;
        },
        enabled: !!tag?.id,
    });

    if (tagLoading || articlesLoading) {
        return (
            <div className="loading">
                <div className="spinner"></div>
            </div>
        );
    }

    if (!tag) {
        return <div className="no-results">Tag not found</div>;
    }

    return (
        <div className="tag-articles-page">
            <div className="tag-header">
                <Tag size={32} />
                <h1>#{tag.name}</h1>
                {tag.description && <p>{tag.description}</p>}
                <span className="tag-count">{tag.articles_count} articles</span>
            </div>

            <div className="articles-grid">
                {articles?.results?.map((article) => (
                    <ArticleCard key={article.id} article={article} />
                ))}
            </div>

            {articles?.results?.length === 0 && (
                <div className="no-results">
                    <p>No articles found with this tag</p>
                </div>
            )}
        </div>
    );
};

export default TagArticles;