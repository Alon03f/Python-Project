from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Article, Comment, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]

class ArticleListSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Article
        fields = ["id", "title", "published_at", "author", "tags"]

class ArticleWriteSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
    class Meta:
        model = Article
        fields = ["id", "title", "content", "tags"]
    def create(self, validated_data):
        tag_names = validated_data.pop("tags", [])
        article = Article.objects.create(author=self.context["request"].user, **validated_data)
        if tag_names:
            tags = [Tag.objects.get_or_create(name=n.strip())[0] for n in tag_names if n.strip()]
            article.tags.set(tags)
        return article
    def update(self, instance, validated_data):
        tag_names = validated_data.pop("tags", None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        if tag_names is not None:
            tags = [Tag.objects.get_or_create(name=n.strip())[0] for n in tag_names if n.strip()]
            instance.tags.set(tags)
        return instance

class ArticleDetailSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Article
        fields = ["id", "title", "content", "published_at", "author", "tags"]

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    class Meta:
        model = Comment
        fields = ["id", "content", "created_at", "user"]
    def create(self, validated_data):
        article = self.context["article"]
        user = self.context["request"].user
        return Comment.objects.create(article=article, user=user, **validated_data)

class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]
