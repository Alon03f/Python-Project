import django_filters
from .models import Article


class ArticleFilter(django_filters.FilterSet):
    """Advanced filtering for articles"""
    title = django_filters.CharFilter(lookup_expr="icontains")
    author = django_filters.CharFilter(field_name="author__username", lookup_expr="icontains")
    tags = django_filters.CharFilter(field_name="tags__name", lookup_expr="iexact")
    published_after = django_filters.DateTimeFilter(field_name="published_at", lookup_expr="gte")
    published_before = django_filters.DateTimeFilter(field_name="published_at", lookup_expr="lte")
    min_views = django_filters.NumberFilter(field_name="views_count", lookup_expr="gte")
    is_published = django_filters.BooleanFilter()
    
    class Meta:
        model = Article
        fields = ["title", "author", "tags", "is_published"]