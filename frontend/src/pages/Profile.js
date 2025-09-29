import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useMutation } from '@tanstack/react-query';
import { User, Mail, MapPin, Globe, Calendar, Save } from 'lucide-react';
import { format } from 'date-fns';
import toast from 'react-hot-toast';
import './Profile.css';

const Profile = () => {
    const { user, updateProfile } = useAuth();
    const [editing, setEditing] = useState(false);
    const [formData, setFormData] = useState({
        first_name: user?.first_name || '',
        last_name: user?.last_name || '',
        email: user?.email || '',
        bio: user?.profile?.bio || '',
        website: user?.profile?.website || '',
        location: user?.profile?.location || '',
    });

    const updateMutation = useMutation({
        mutationFn: async (data) => {
            await updateProfile(data);
        },
        onSuccess: () => {
            toast.success('Profile updated successfully!');
            setEditing(false);
        },
        onError: (error) => {
            toast.error(error.response?.data?.message || 'Failed to update profile');
        },
    });

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        updateMutation.mutate(formData);
    };

    const handleCancel = () => {
        setFormData({
            first_name: user?.first_name || '',
            last_name: user?.last_name || '',
            email: user?.email || '',
            bio: user?.profile?.bio || '',
            website: user?.profile?.website || '',
            location: user?.profile?.location || '',
        });
        setEditing(false);
    };

    return (
        <div className="profile-container">
            <div className="profile-card">
                <div className="profile-header">
                    <div className="profile-avatar">
                        <User size={64} />
                    </div>
                    <h1>{user?.username}</h1>
                    <p className="profile-name">
                        {user?.first_name} {user?.last_name}
                    </p>
                </div>

                {!editing ? (
                    <div className="profile-info">
                        <div className="info-item">
                            <Mail size={18} />
                            <span>{user?.email}</span>
                        </div>

                        {user?.profile?.location && (
                            <div className="info-item">
                                <MapPin size={18} />
                                <span>{user.profile.location}</span>
                            </div>
                        )}

                        {user?.profile?.website && (
                            <div className="info-item">
                                <Globe size={18} />
                                <a href={user.profile.website} target="_blank" rel="noopener noreferrer">
                                    {user.profile.website}
                                </a>
                            </div>
                        )}

                        <div className="info-item">
                            <Calendar size={18} />
                            <span>Joined {format(new Date(user?.date_joined), 'MMMM yyyy')}</span>
                        </div>

                        {user?.profile?.bio && (
                            <div className="profile-bio">
                                <h3>Bio</h3>
                                <p>{user.profile.bio}</p>
                            </div>
                        )}

                        <div className="profile-stats">
                            <div className="stat-item">
                                <strong>{user?.articles_count || 0}</strong>
                                <span>Articles</span>
                            </div>
                            <div className="stat-item">
                                <strong>{user?.comments_count || 0}</strong>
                                <span>Comments</span>
                            </div>
                        </div>

                        <button onClick={() => setEditing(true)} className="btn btn-primary">
                            Edit Profile
                        </button>
                    </div>
                ) : (
                    <form onSubmit={handleSubmit} className="profile-form">
                        <div className="form-row">
                            <div className="form-group">
                                <label htmlFor="first_name">First Name</label>
                                <input
                                    type="text"
                                    id="first_name"
                                    name="first_name"
                                    value={formData.first_name}
                                    onChange={handleChange}
                                    className="form-control"
                                />
                            </div>

                            <div className="form-group">
                                <label htmlFor="last_name">Last Name</label>
                                <input
                                    type="text"
                                    id="last_name"
                                    name="last_name"
                                    value={formData.last_name}
                                    onChange={handleChange}
                                    className="form-control"
                                />
                            </div>
                        </div>

                        <div className="form-group">
                            <label htmlFor="email">Email</label>
                            <input
                                type="email"
                                id="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                className="form-control"
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="location">Location</label>
                            <input
                                type="text"
                                id="location"
                                name="location"
                                value={formData.location}
                                onChange={handleChange}
                                className="form-control"
                                placeholder="e.g. New York, USA"
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="website">Website</label>
                            <input
                                type="url"
                                id="website"
                                name="website"
                                value={formData.website}
                                onChange={handleChange}
                                className="form-control"
                                placeholder="https://example.com"
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="bio">Bio</label>
                            <textarea
                                id="bio"
                                name="bio"
                                value={formData.bio}
                                onChange={handleChange}
                                className="form-control"
                                rows="4"
                                placeholder="Tell us about yourself..."
                            />
                        </div>

                        <div className="form-actions">
                            <button
                                type="submit"
                                className="btn btn-success"
                                disabled={updateMutation.isPending}
                            >
                                <Save size={18} />
                                {updateMutation.isPending ? 'Saving...' : 'Save Changes'}
                            </button>
                            <button type="button" onClick={handleCancel} className="btn btn-secondary">
                                Cancel
                            </button>
                        </div>
                    </form>
                )}
            </div>
        </div>
    );
};

export default Profile;