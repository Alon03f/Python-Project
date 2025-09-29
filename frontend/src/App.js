import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import ArticleDetail from './pages/ArticleDetail';
import Login from './pages/Login';
import Register from './pages/Register';
import CreateArticle from './pages/CreateArticle';
import EditArticle from './pages/EditArticle';
import Profile from './pages/Profile';
import Bookmarks from './pages/Bookmarks';
import TagArticles from './pages/TagArticles';
import UserArticles from './pages/UserArticles';
import PrivateRoute from './components/PrivateRoute';
import AdminRoute from './components/AdminRoute';

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/articles/:slug" element={<ArticleDetail />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/tags/:slug" element={<TagArticles />} />
        <Route path="/users/:userId/articles" element={<UserArticles />} />

        <Route path="/profile" element={<PrivateRoute><Profile /></PrivateRoute>} />
        <Route path="/bookmarks" element={<PrivateRoute><Bookmarks /></PrivateRoute>} />

        <Route path="/articles/create" element={<AdminRoute><CreateArticle /></AdminRoute>} />
        <Route path="/articles/:id/edit" element={<AdminRoute><EditArticle /></AdminRoute>} />
      </Routes>
    </Layout>
  );
}

export default App;