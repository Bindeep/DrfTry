from rest_framework import viewsets
from .serializers import BlogSerializer, ArticleSerializer, CommentSerializer
from ..models.blog import Blog
from ..models.articles import Article, Comment
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.db.models import F
from rest_framework.response import Response

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


@api_view(['PATCH', ])
def increase_like(request, id):
    
    liked = False
    if request.method == 'PATCH':
        article_obj = get_object_or_404(Article, id=id)
        if article_obj:
            article_obj.like += 1 
            article_obj.save(update_fields=['like', ])
            liked = True
            return Response({'liked': liked, 'count': article_obj.like})
    else:
        return Response({'liked': liked})