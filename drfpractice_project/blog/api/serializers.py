from rest_framework import serializers
from ..models.blog import Blog
from ..models.articles import Article, Comment, Like
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
        fields = ('id', 'title', 'content', 'created_at', 'author', 'articles', 'get_name')
 

# class ArticleSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Article
#         fields = (
#             'id',
#             'name',
#             'content',
#             'blog',
#             'author',
#             'is_published',
#             'like',
#             'created_time',
#             'updated_time',
#             'get_author'
#         )





class ArticleSerializer(serializers.ModelSerializer):

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        request = self.context.get('request')
        if not request.user.is_superuser:
            if request.method ==  ['POST', 'PUT']:
                fields.pop('is_published')
                fields.pop('author')
            elif request.method == 'PUT':
                fields.pop('author')
                fields.pop('is_published')
                fields.pop('blog')
        return fields
    
    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data.update(
            {
                'author': user,
            }
        )
        return super().create(validated_data)

    class Meta:
        model = Article
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        lookup_field = 'article_id'
        extra_kwargs = {
            'url': {'lookup_field': 'article_id'}
        }

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'