import React from 'react';
import { Link } from 'react-router-dom';
import { Heart, MessageCircle, Eye, Clock, User } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import './ArticleCard.css';

const ArticleCard = ({ article }) => {
    return (
        <div className="article-card">
            {article.featured_image && (
                <Link to={`/articles/${article.slug}`} className="article-image-link">
                    <img src={article.featured_image} alt={article.title} className="article-image" />
                </Link>
            )}

            <div className="article-content">
                <div className="article-tags">
                    {article.tags?.slice(0, 3).map((tag) => (
                        <Link key={tag.id} to={`/tags/${tag.slug}`} className="badge">
                            {tag.name}
                        </Link>
                    ))}
                </div>

                <Link to={`/articles/${article.slug}`} className="article-title-link">
                    <h2 className="article-title">{article.title}</h2>
                </Link>

                <p className="article-excerpt">{article.excerpt}</p>

                <div className="article-meta">
                    <Link to={`/users/${article.author.id}/articles`} className="article-author">
                        <User size={16} />
                        <span>{article.author.username}</span>
                    </Link>

                    <div className="article-stats">
                        <span className="stat">
                            <Eye size={16} />
                            {article.views_count}
                        </span>
                        <span className="stat">
                            <Heart size={16} />
                            {article.likes_count}
                        </span>
                        <span className="stat">
                            <MessageCircle size={16} />
                            {article.comments_count}
                        </span>
                        <span className="stat">
                            <Clock size={16} />
                            {article.read_time} min
                        </span>
                    </div>
                </div>

                <div className="article-date">
                    {formatDistanceToNow(new Date(article.published_at), { addSuffix: true })}
                </div>
            </div>
        </div>
    );
};

export default ArticleCard;