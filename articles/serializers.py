def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
    
    def get_is_bookmarked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.bookmarks.filter(user=request.user).exists()
        return False
    
    def get_read_time(self, obj):
        """Calculate estimated reading time in minutes"""
        words_per_minute = 200
        word_count = len(obj.content.split())
        minutes = word_count // words_per_minute
        return max(1, minutes)


class ArticleDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed article view"""
    author = AuthorSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField()
    read_time = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = [
            "id", "slug", "title", "content", "excerpt", "featured_image",
            "published_at", "updated_at", "author", "tags", "views_count",
            "likes_count", "comments_count", "is_liked", "is_bookmarked",
            "read_time", "is_published"
        ]
        read_only_fields = ["slug", "published_at", "views_count"]
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
    
    def get_is_bookmarked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.bookmarks.filter(user=request.user).exists()
        return False
    
    def get_read_time(self, obj):
        words_per_minute = 200
        word_count = len(obj.content.split())
        minutes = word_count // words_per_minute
        return max(1, minutes)


class ArticleWriteSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating articles"""
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        write_only=True,
        required=False,
        allow_empty=True
    )
    
    class Meta:
        model = Article
        fields = ["id", "title", "content", "excerpt", "featured_image", "tags", "is_published"]
    
    def validate_tags(self, value):
        """Validate tags list"""
        if len(value) > 10:
            raise serializers.ValidationError("Maximum 10 tags allowed")
        return value
    
    def validate_title(self, value):
        """Validate title uniqueness for new articles"""
        if not self.instance:
            if Article.objects.filter(title__iexact=value).exists():
                raise serializers.ValidationError("An article with this title already exists")
        return value
    
    def create(self, validated_data):
        tag_names = validated_data.pop("tags", [])
        article = Article.objects.create(author=self.context["request"].user, **validated_data)
        
        if tag_names:
            tags = []
            for name in tag_names:
                name = name.strip().lower()
                if name:
                    tag, _ = Tag.objects.get_or_create(name=name)
                    tags.append(tag)
            article.tags.set(tags)
        
        return article
    
    def update(self, instance, validated_data):
        tag_names = validated_data.pop("tags", None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if tag_names is not None:
            tags = []
            for name in tag_names:
                name = name.strip().lower()
                if name:
                    tag, _ = Tag.objects.get_or_create(name=name)
                    tags.append(tag)
            instance.tags.set(tags)
        
        return instance


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments"""
    user = AuthorSerializer(read_only=True)
    replies_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            "id", "content", "created_at", "updated_at", "user",
            "parent", "is_edited", "replies_count"
        ]
        read_only_fields = ["created_at", "updated_at", "is_edited"]
    
    def get_replies_count(self, obj):
        return obj.replies.count()
    
    def validate_parent(self, value):
        """Validate parent comment belongs to same article"""
        if value:
            article_id = self.context.get("article_id")
            if value.article_id != article_id:
                raise serializers.ValidationError("Parent comment must belong to the same article")
            if value.parent is not None:
                raise serializers.ValidationError("Cannot reply to a reply (max depth is 2)")
        return value
    
    def create(self, validated_data):
        article_id = self.context["article_id"]
        user = self.context["request"].user
        article = Article.objects.get(id=article_id)
        return Comment.objects.create(article=article, user=user, **validated_data)


class CommentDetailSerializer(serializers.ModelSerializer):
    """Serializer for comment with replies"""
    user = AuthorSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            "id", "content", "created_at", "updated_at", "user",
            "parent", "is_edited", "replies"
        ]
        read_only_fields = ["created_at", "updated_at", "is_edited"]
    
    def get_replies(self, obj):
        if obj.parent is None:
            replies = obj.replies.all()
            return CommentSerializer(replies, many=True, context=self.context).data
        return []


class ArticleLikeSerializer(serializers.ModelSerializer):
    """Serializer for article likes"""
    user = AuthorSerializer(read_only=True)
    
    class Meta:
        model = ArticleLike
        fields = ["id", "user", "created_at"]
        read_only_fields = ["created_at"]


class BookmarkSerializer(serializers.ModelSerializer):
    """Serializer for bookmarks"""
    article = ArticleListSerializer(read_only=True)
    
    class Meta:
        model = Bookmark
        fields = ["id", "article", "created_at"]
        read_only_fields = ["created_at"]