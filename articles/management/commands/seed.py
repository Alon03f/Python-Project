from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from articles.models import Article, Comment, Tag, ArticleLike, Bookmark
from accounts.models import UserProfile
import random


class Command(BaseCommand):
    help = "Seed database with sample data"
    
    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")
        
        # Create admin user
        admin, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "first_name": "Admin",
                "last_name": "User",
                "is_staff": True,
                "is_superuser": True
            }
        )
        if created or not admin.has_usable_password():
            admin.set_password("admin123")
            admin.save()
            self.stdout.write(self.style.SUCCESS(f"✓ Admin user created: admin/admin123"))
        
        # Create regular users
        users_data = [
            ("alice", "alice@example.com", "Alice", "Johnson"),
            ("bob", "bob@example.com", "Bob", "Smith"),
            ("charlie", "charlie@example.com", "Charlie", "Brown"),
            ("diana", "diana@example.com", "Diana", "Prince"),
        ]
        
        users = []
        for username, email, first_name, last_name in users_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name
                }
            )
            if created or not user.has_usable_password():
                user.set_password(f"{username}123")
                user.save()
            users.append(user)
            
            # Update profile
            profile = user.profile
            profile.bio = f"Hi, I'm {first_name}! I love writing about technology and science."
            profile.location = random.choice(["New York", "London", "Tokyo", "Paris", "Berlin"])
            profile.save()
        
        self.stdout.write(self.style.SUCCESS(f"✓ Created {len(users)} regular users"))
        
        # Create tags
        tags_data = [
            ("python", "Python programming language"),
            ("django", "Django web framework"),
            ("javascript", "JavaScript programming"),
            ("react", "React.js library"),
            ("technology", "General technology topics"),
            ("tutorial", "How-to guides and tutorials"),
            ("news", "Tech news and updates"),
            ("ai", "Artificial Intelligence"),
            ("webdev", "Web Development"),
            ("database", "Database systems"),
        ]
        
        tags = []
        for name, description in tags_data:
            tag, _ = Tag.objects.get_or_create(name=name, defaults={"description": description})
            tags.append(tag)
        
        self.stdout.write(self.style.SUCCESS(f"✓ Created {len(tags)} tags"))
        
        # Create articles
        if Article.objects.count() == 0:
            articles_data = [
                {
                    "title": "Getting Started with Django REST Framework",
                    "content": """Django REST Framework is a powerful toolkit for building Web APIs. 
                    It provides features like authentication, serialization, and viewsets that make API development quick and easy.
                    
                    In this tutorial, we'll cover the basics of setting up a REST API with Django. 
                    We'll create models, serializers, and views to handle CRUD operations.
                    
                    Let's dive in and explore how to build professional APIs with Django!""",
                    "author": admin,
                    "tags": [tags[0], tags[1], tags[5]],
                },
                {
                    "title": "10 Python Tips Every Developer Should Know",
                    "content": """Python is an amazing language with many hidden features. 
                    Here are 10 tips that will make you a more productive Python developer:
                    
                    1. Use list comprehensions for cleaner code
                    2. Leverage context managers with 'with' statement
                    3. Use enumerate() instead of range(len())
                    4. Master dictionary comprehensions
                    5. Understand generator expressions
                    
                    And 5 more tips that will change how you write Python code!""",
                    "author": users[0],
                    "tags": [tags[0], tags[5]],
                },
                {
                    "title": "The Future of AI in 2025",
                    "content": """Artificial Intelligence is evolving rapidly. 
                    In 2025, we're seeing breakthroughs in natural language processing, computer vision, and robotics.
                    
                    Machine learning models are becoming more efficient and accessible.
                    Companies are integrating AI into everyday products.
                    
                    What does this mean for developers? More opportunities and exciting challenges ahead!""",
                    "author": users[1],
                    "tags": [tags[4], tags[6], tags[7]],
                },
                {
                    "title": "Building Modern Web Apps with React",
                    "content": """React has revolutionized front-end development. 
                    Its component-based architecture makes building complex UIs manageable.
                    
                    In this article, we explore React hooks, state management, and best practices 
                    for building scalable applications.
                    
                    Whether you're new to React or an experienced developer, there's always something new to learn!""",
                    "author": users[2],
                    "tags": [tags[2], tags[3], tags[8]],
                },
                {
                    "title": "Database Optimization Techniques",
                    "content": """Database performance is crucial for web applications. 
                    Learn how to optimize queries, use indexes effectively, and design efficient schemas.
                    
                    We'll cover PostgreSQL optimization, query planning, and common pitfalls to avoid.
                    
                    These techniques will help you build faster, more scalable applications!""",
                    "author": users[3],
                    "tags": [tags[9], tags[5]],
                },
                {
                    "title": "Introduction to JWT Authentication",
                    "content": """JSON Web Tokens (JWT) are a popular method for securing APIs. 
                    They provide a stateless authentication mechanism that scales well.
                    
                    In this guide, we'll implement JWT authentication in Django REST Framework,
                    covering token generation, validation, and refresh strategies.
                    
                    Security is paramount in modern web applications!""",
                    "author": admin,
                    "tags": [tags[1], tags[5], tags[4]],
                },
            ]
            
            created_articles = []
            for article_data in articles_data:
                article_tags = article_data.pop("tags")
                article = Article.objects.create(**article_data)
                article.tags.set(article_tags)
                article.views_count = random.randint(50, 500)
                article.save()
                created_articles.append(article)
            
            self.stdout.write(self.style.SUCCESS(f"✓ Created {len(created_articles)} articles"))
            
            # Create comments
            comments_data = [
                "Great article! Very helpful.",
                "Thanks for sharing this.",
                "I learned a lot from this post.",
                "Could you elaborate more on this topic?",
                "This is exactly what I was looking for!",
                "Excellent explanation!",
                "Very informative, thank you!",
                "I have a question about the implementation...",
                "This helped me solve my problem!",
                "Looking forward to more content like this.",
            ]
            
            comment_count = 0
            for article in created_articles:
                num_comments = random.randint(2, 5)
                for _ in range(num_comments):
                    Comment.objects.create(
article=article,
                        user=random.choice(users + [admin]),
                        content=random.choice(comments_data)
                    )
                    comment_count += 1
            
            self.stdout.write(self.style.SUCCESS(f"✓ Created {comment_count} comments"))
            
            # Create likes
            like_count = 0
            for article in created_articles:
                num_likes = random.randint(1, len(users))
                likers = random.sample(users, num_likes)
                for user in likers:
                    ArticleLike.objects.get_or_create(article=article, user=user)
                    like_count += 1
            
            self.stdout.write(self.style.SUCCESS(f"✓ Created {like_count} likes"))
            
            # Create bookmarks
            bookmark_count = 0
            for article in created_articles:
                num_bookmarks = random.randint(0, len(users))
                bookmarkers = random.sample(users, num_bookmarks)
                for user in bookmarkers:
                    Bookmark.objects.get_or_create(article=article, user=user)
                    bookmark_count += 1
            
            self.stdout.write(self.style.SUCCESS(f"✓ Created {bookmark_count} bookmarks"))
        
        self.stdout.write(self.style.SUCCESS("\n✅ Database seeded successfully!"))
        self.stdout.write(self.style.WARNING("\nLogin credentials:"))
        self.stdout.write("  Admin: admin / admin123")
        self.stdout.write("  Users: alice/alice123, bob/bob123, charlie/charlie123, diana/diana123")