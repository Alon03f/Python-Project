import React, { useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import {
    Heart,
    Bookmark,
    Eye,
    Clock,
    User,
    Calendar,
    Edit,
    Trash2,
    MessageCircle,
    Send
} from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import toast from 'react-hot-toast';
import './ArticleDetail.css';

const ArticleDetail = () => {
    const { slug } = useParams();
    const { user, isAdmin } = useAuth();
    const navigate = useNavigate();
    const queryClient = useQueryClient();
    const [commentContent, setCommentContent] = useState('');
    const [replyTo, setReplyTo] = useState(null);

    const { data: article, isLoading } = useQuery({
        queryKey: ['article', slug],
        queryFn: async () => {
            const response = await api.get(`/api/articles/${slug}/`);
            return response.data;
        },
    });

    const { data: comments } = useQuery({
        queryKey: ['comments', article?.id],
        queryFn: async () => {
            const response = await api.get(`/api/articles/${article.id}/comments/`);
            return response.data;
        },
        enabled: !!article?.id,
    });

    const likeMutation = useMutation({
        mutationFn: async () => {
            await api.post(`/api/articles/${article.id}/like/`);
        },
        onSuccess: () => {
            queryClient.invalidateQueries(['article', slug]);
            toast.success(article.is_liked ? 'Article unliked' : 'Article liked!');
        },
    });

    const bookmarkMutation = useMutation({
        mutationFn: async () => {
            await api.post(`/api/articles/${article.id}/bookmark/`);
        },
        onSuccess: () => {
            queryClient.invalidateQueries(['article', slug]);
            toast.success(article.is_bookmarked ? 'Bookmark removed' : 'Article bookmarked!');
        },
    });

    const commentMutation = useMutation({
        mutationFn: async (commentData) => {
            await api.post(`/api/articles/${article.id}/add_comment/`, commentData);
        },
        onSuccess: () => {
            queryClient.invalidateQueries(['comments', article.id]);
            queryClient.invalidateQueries(['article', slug]);
            setCommentContent('');
            setReplyTo(null);
            toast.success('Comment added!');
        },
    });

    const deleteCommentMutation = useMutation({
        mutationFn: async (commentId) => {
            await api.delete(`/api/comments/${commentId}/`);
        },
        onSuccess: () => {
            queryClient.invalidateQueries(['comments', article.id]);
            queryClient.invalidateQueries(['article', slug]);
            toast.success('Comment deleted');
        },
    });

    const deleteArticleMutation = useMutation({
        mutationFn: async () => {
            await api.delete(`/api/articles/${article.id}/`);
        },
        onSuccess: () => {
            toast.success('Article deleted');
            navigate('/');
        },
    });

    const handleLike = () => {
        if (!user) {
            toast.error('Please login to like articles');
            return;
        }
        likeMutation.mutate();
    };

    const handleBookmark = () => {
        if (!user) {
            toast.error('Please login to bookmark articles');
            return;
        }
        bookmarkMutation.mutate();
    };

    const handleCommentSubmit = (e) => {
        e.preventDefault();
        if (!user) {
            toast.error('Please login to comment');
            return;
        }
        if (!commentContent.trim()) {
            toast.error('Comment cannot be empty');
            return;
        }

        commentMutation.mutate({
            content: commentContent,
            parent: replyTo,
        });
    };

    const handleDeleteArticle = () => {
        if (window.confirm('Are you sure you want to delete this article?')) {
            deleteArticleMutation.mutate();
        }
    };

    const handleDeleteComment = (commentId) => {
        if (window.confirm('Are you sure you want to delete this comment?')) {
            deleteCommentMutation.mutate(commentId);
        }
    };

    if (isLoading) {
        return (
            <div className="loading">
                <div className="spinner"></div>
            </div>
        );
    }

    if (!article) {
        return <div className="no-results">Article not found</div>;
    }

    return (
        <div className="article-detail">
            <article className="article-content-wrapper">
                <div className="article-header">
                    <div className="article-tags">
                        {article.tags?.map((tag) => (
                            <Link key={tag.id} to={`/tags/${tag.slug}`} className="badge">
                                {tag.name}
                            </Link>
                        ))}
                    </div>

                    <h1 className="article-main-title">{article.title}</h1>

                    <div className="article-meta-info">
                        <Link to={`/users/${article.author.id}/articles`} className="author-info">
                            <User size={18} />
                            <span>{article.author.username}</span>
                        </Link>

                        <div className="meta-stats">
                            <span className="meta-item">
                                <Calendar size={16} />
                                {formatDistanceToNow(new Date(article.published_at), { addSuffix: true })}
                            </span>
                            <span className="meta-item">
                                <Clock size={16} />
                                {article.read_time} min read
                            </span>
                            <span className="meta-item">
                                <Eye size={16} />
                                {article.views_count} views
                            </span>
                        </div>
                    </div>

                    {article.featured_image && (
                        <img
                            src={article.featured_image}
                            alt={article.title}
                            className="featured-image"
                        />
                    )}
                </div>

                <div
                    className="article-body"
                    dangerouslySetInnerHTML={{ __html: article.content }}
                />

                <div className="article-actions">
                    <button
                        onClick={handleLike}
                        className={`action-btn ${article.is_liked ? 'active' : ''}`}
                    >
                        <Heart size={20} fill={article.is_liked ? 'currentColor' : 'none'} />
                        <span>{article.likes_count} Likes</span>
                    </button>

                    <button
                        onClick={handleBookmark}
                        className={`action-btn ${article.is_bookmarked ? 'active' : ''}`}
                    >
                        <Bookmark size={20} fill={article.is_bookmarked ? 'currentColor' : 'none'} />
                        <span>{article.is_bookmarked ? 'Bookmarked' : 'Bookmark'}</span>
                    </button>

                    <span className="action-btn">
                        <MessageCircle size={20} />
                        <span>{article.comments_count} Comments</span>
                    </span>

                    {isAdmin && (
                        <>
                            <Link to={`/articles/${article.id}/edit`} className="action-btn edit-btn">
                                <Edit size={20} />
                                <span>Edit</span>
                            </Link>

                            <button onClick={handleDeleteArticle} className="action-btn delete-btn">
                                <Trash2 size={20} />
                                <span>Delete</span>
                            </button>
                        </>
                    )}
                </div>
            </article>

            <section className="comments-section">
                <h2 className="comments-title">
                    Comments ({article.comments_count})
                </h2>

                {user && (
                    <form onSubmit={handleCommentSubmit} className="comment-form">
                        {replyTo && (
                            <div className="reply-indicator">
                                <span>Replying to a comment</span>
                                <button
                                    type="button"
                                    onClick={() => setReplyTo(null)}
                                    className="btn-cancel-reply"
                                >
                                    Cancel
                                </button>
                            </div>
                        )}
                        <textarea
                            value={commentContent}
                            onChange={(e) => setCommentContent(e.target.value)}
                            placeholder="Write a comment..."
                            className="comment-textarea"
                            rows="4"
                        />
                        <button type="submit" className="btn btn-primary" disabled={commentMutation.isPending}>
                            <Send size={16} />
                            {commentMutation.isPending ? 'Posting...' : 'Post Comment'}
                        </button>
                    </form>
                )}

                <div className="comments-list">
                    {comments?.map((comment) => (
                        <div key={comment.id} className="comment">
                            <div className="comment-header">
                                <div className="comment-author">
                                    <User size={16} />
                                    <strong>{comment.user.username}</strong>
                                    <span className="comment-date">
                                        {formatDistanceToNow(new Date(comment.created_at), { addSuffix: true })}
                                    </span>
                                    {comment.is_edited && <span className="edited-badge">(edited)</span>}
                                </div>

                                {(user?.id === comment.user.id || isAdmin) && (
                                    <button
                                        onClick={() => handleDeleteComment(comment.id)}
                                        className="btn-delete-comment"
                                    >
                                        <Trash2 size={14} />
                                    </button>
                                )}
                            </div>

                            <p className="comment-content">{comment.content}</p>

                            {user && (
                                <button
                                    onClick={() => setReplyTo(comment.id)}
                                    className="btn-reply"
                                >
                                    Reply
                                </button>
                            )}

                            {comment.replies && comment.replies.length > 0 && (
                                <div className="replies">
                                    {comment.replies.map((reply) => (
                                        <div key={reply.id} className="comment reply">
                                            <div className="comment-header">
                                                <div className="comment-author">
                                                    <User size={14} />
                                                    <strong>{reply.user.username}</strong>
                                                    <span className="comment-date">
                                                        {formatDistanceToNow(new Date(reply.created_at), { addSuffix: true })}
                                                    </span>
                                                    {reply.is_edited && <span className="edited-badge">(edited)</span>}
                                                </div>

                                                {(user?.id === reply.user.id || isAdmin) && (
                                                    <button
                                                        onClick={() => handleDeleteComment(reply.id)}
                                                        className="btn-delete-comment"
                                                    >
                                                        <Trash2 size={14} />
                                                    </button>
                                                )}
                                            </div>

                                            <p className="comment-content">{reply.content}</p>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    ))}

                    {comments?.length === 0 && (
                        <p className="no-comments">No comments yet. Be the first to comment!</p>
                    )}
                </div>
            </section>
        </div>
    );
};

export default ArticleDetail;