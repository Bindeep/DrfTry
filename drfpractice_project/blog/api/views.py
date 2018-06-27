from rest_framework import viewsets
from .serializers import BlogSerializer, ArticleSerializer, CommentSerializer
from ..models.blog import Blog
from ..models.articles import Article, Comment
from rest_framework.generics import ListAPIView

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer