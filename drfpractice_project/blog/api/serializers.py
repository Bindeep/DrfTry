from rest_framework import serializers
from ..models.blog import Blog
from ..models.articles import Article, Comment
from django.contrib.auth.models import User

class BlogRelatedArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ( 'blog' ,'id', 'name')


class BlogSerializer(serializers.ModelSerializer):

    # articles = serializers.StringRelatedField(
    #     many=True,
    #     # view_name='article-detail',
    #     # read_only=True,
    # )
    articles = BlogRelatedArticleSerializer(many=True)
    class Meta:
        model = Blog
        fields = ('id', 'title', 'content', 'created_at', 'created_by', 'articles', 'get_name')
 

class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = (
            'id',
            'name',
            'content',
            'blog',
            'author',
            'is_published',
            'like',
            'created_time',
            'updated_time',
            'get_author'
        )


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'