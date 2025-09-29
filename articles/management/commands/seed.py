from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from articles.models import Article, Comment, Tag

class Command(BaseCommand):
    def handle(self, *args, **options):
        users_group, _ = Group.objects.get_or_create(name="users")
        editors_group, _ = Group.objects.get_or_create(name="editors")
        admins_group, _ = Group.objects.get_or_create(name="admins")

        admin, _ = User.objects.get_or_create(username="admin", defaults={"email": "admin@example.com", "is_staff": True, "is_superuser": True})
        if not admin.has_usable_password():
            admin.set_password("admin123")
            admin.save()
        admin.groups.add(admins_group)

        u1, created = User.objects.get_or_create(username="alice", defaults={"email": "alice@example.com"})
        if created:
            u1.set_password("alice123")
            u1.save()
        u1.groups.add(users_group)

        u2, created = User.objects.get_or_create(username="bob", defaults={"email": "bob@example.com"})
        if created:
            u2.set_password("bob123")
            u2.save()
        u2.groups.add(users_group)

        t_python, _ = Tag.objects.get_or_create(name="python")
        t_django, _ = Tag.objects.get_or_create(name="django")
        t_news, _ = Tag.objects.get_or_create(name="news")

        if Article.objects.count() == 0:
            a1 = Article.objects.create(title="ברוכים הבאים לבלוג", content="תוכן ראשון", author=admin)
            a1.tags.set([t_news])
            a2 = Article.objects.create(title="מדריך Django REST", content="תוכן שני", author=admin)
            a2.tags.set([t_python, t_django])

            Comment.objects.create(article=a1, user=u1, content="מעולה")
            Comment.objects.create(article=a1, user=u2, content="תודה")
            Comment.objects.create(article=a2, user=u1, content="שימושי")
            Comment.objects.create(article=a2, user=u2, content="אהבתי")
