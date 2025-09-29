import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '../services/api';
import ArticleCard from '../components/ArticleCard';
import { Search, TrendingUp, Tag } from 'lucide-react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const [currentPage, setCurrentPage] = useState(1);

    const { data: articlesData, isLoading } = useQuery({
        queryKey: ['articles', currentPage, searchTerm],
        queryFn: async () => {
            const response = await api.get('/api/articles/', {
                params: {
                    page: currentPage,
                    search: searchTerm || undefined,
                },
            });
            return response.data;
        },
    });

    const { data: tagsData } = useQuery({
        queryKey: ['tags'],
        queryFn: async () => {
            const response = await api.get('/api/tags/');
            return response.data;
        },
    });

    const { data: popularArticles } = useQuery({
        queryKey: ['popular-articles'],
        queryFn: async () => {
            const response = await api.get('/api/articles/popular/');
            return response.data;
        },
    });

    const handleSearch = (e) => {
        e.preventDefault();
        setCurrentPage(1);
    };

    if (isLoading) {
        return (
            <div className="loading">
                <div className="spinner"></div>
            </div>
        );
    }

    return (
        <div className="home">
            <div className="hero">
                <h1>Welcome to Our Blog</h1>
                <p>Discover articles about technology, programming, and more</p>

                <form onSubmit={handleSearch} className="search-form">
                    <div className="search-input-wrapper">
                        <Search className="search-icon" size={20} />
                        <input
                            type="text"
                            placeholder="Search articles..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            className="search-input"
                        />
                    </div>
                    <button type="submit" className="btn btn-primary">
                        Search
                    </button>
                </form>
            </div>

            <div className="home-content">
                <div className="main-content">
                    <div className="section-header">
                        <h2>Latest Articles</h2>
                    </div>

                    <div className="articles-grid">
                        {articlesData?.results?.map((article) => (
                            <ArticleCard key={article.id} article={article} />
                        ))}
                    </div>

                    {articlesData?.results?.length === 0 && (
                        <div className="no-results">
                            <p>No articles found</p>
                        </div>
                    )}

                    {articlesData && (articlesData.next || articlesData.previous) && (
                        <div className="pagination">
                            <button
                                onClick={() => setCurrentPage((prev) => prev - 1)}
                                disabled={!articlesData.previous}
                                className="btn btn-secondary"
                            >
                                Previous
                            </button>
                            <span className="page-info">Page {currentPage}</span>
                            <button
                                onClick={() => setCurrentPage((prev) => prev + 1)}
                                disabled={!articlesData.next}
                                className="btn btn-secondary"
                            >
                                Next
                            </button>
                        </div>
                    )}
                </div>

                <aside className="sidebar">
                    <div className="sidebar-card">
                        <h3 className="sidebar-title">
                            <TrendingUp size={20} />
                            Popular Articles
                        </h3>
                        <div className="popular-list">
                            {popularArticles?.slice(0, 5).map((article) => (
                                <Link
                                    key={article.id}
                                    to={`/articles/${article.slug}`}
                                    className="popular-item"
                                >
                                    <h4>{article.title}</h4>
                                    <span className="popular-views">{article.views_count} views</span>
                                </Link>
                            ))}
                        </div>
                    </div>

                    <div className="sidebar-card">
                        <h3 className="sidebar-title">
                            <Tag size={20} />
                            Popular Tags
                        </h3>
                        <div className="tags-list">
                            {tagsData?.results?.slice(0, 15).map((tag) => (
                                <Link key={tag.id} to={`/tags/${tag.slug}`} className="badge">
                                    {tag.name} ({tag.articles_count})
                                </Link>
                            ))}
                        </div>
                    </div>
                </aside>
            </div>
        </div>
    );
};

export default Home;