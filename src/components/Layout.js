import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Home, BookMarked, User, LogOut, LogIn, UserPlus, PenSquare } from 'lucide-react';
import './Layout.css';

const Layout = ({ children }) => {
    const { user, logout, isAdmin } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/');
    };

    return (
        <div className="layout">
            <header className="header">
                <div className="container header-content">
                    <Link to="/" className="logo">
                        <PenSquare size={24} />
                        <span>Blog API</span>
                    </Link>

                    <nav className="nav">
                        <Link to="/" className="nav-link">
                            <Home size={18} />
                            <span>Home</span>
                        </Link>

                        {user ? (
                            <>
                                {isAdmin && (
                                    <Link to="/articles/create" className="nav-link">
                                        <PenSquare size={18} />
                                        <span>Write</span>
                                    </Link>
                                )}
                                <Link to="/bookmarks" className="nav-link">
                                    <BookMarked size={18} />
                                    <span>Bookmarks</span>
                                </Link>
                                <Link to="/profile" className="nav-link">
                                    <User size={18} />
                                    <span>Profile</span>
                                </Link>
                                <button onClick={handleLogout} className="nav-link nav-button">
                                    <LogOut size={18} />
                                    <span>Logout</span>
                                </button>
                            </>
                        ) : (
                            <>
                                <Link to="/login" className="nav-link">
                                    <LogIn size={18} />
                                    <span>Login</span>
                                </Link>
                                <Link to="/register" className="nav-link">
                                    <UserPlus size={18} />
                                    <span>Register</span>
                                </Link>
                            </>
                        )}
                    </nav>
                </div>
            </header>

            <main className="main">
                <div className="container">{children}</div>
            </main>

            <footer className="footer">
                <div className="container">
                    <p>&copy; 2025 Blog API. Built with Django REST Framework & React.</p>
                </div>
            </footer>
        </div>
    );
};

export default Layout;