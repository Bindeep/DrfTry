from rest_framework import serializers
from ..models.blog import Blog
from ..models.articles import Article, Comment, Like


class BlogRelatedArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('blog', 'id', 'name')


class BlogSerializer(serializers.ModelSerializer):

    # articles = serializers.StringRelatedField(
    #     many=True,
    #     # view_name='article-detail',
    #     # read_only=True,
    # )
    articles = BlogRelatedArticleSerializer(many=True, read_only=True)

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

class CommentSerializer(serializers.ModelSerializer):

    is_user_comment = serializers.SerializerMethodField(read_only=True)

    def get_is_user_comment(self, obj):
        return obj.commented_by == self.context['request'].user

    class Meta:
        model = Comment
        fields = ['id', 'content', 'commented_by_name', 'commented_by', 'is_user_comment']

    # def create(self, validated_data):
    #     request = self.context['request']
    #     validated_data['commented_by'] = request.user
    #     import ipdb; ipdb.set_trace()
    #     article_id = request.parser_context.get('kwargs').get('pk')
    #     validated_data['article'] = Article.objects.get(pk=article_id)
    #     import ipdb; ipdb.set_trace()


class ArticleSerializer(serializers.ModelSerializer):

    created_at = serializers.SerializerMethodField()
    has_user_liked = serializers.SerializerMethodField()
    article_comments = CommentSerializer(many=True)

    def get_created_at(self, obj):
        created_at = obj.created_at.strftime("%A %d. %B %Y")
        return created_at

    def get_has_user_liked(self, obj):
        user = self.context['request'].user
        return obj.article_likes.filter(user=user).exists()

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        request = self.context.get('request')
        if not request.user.is_superuser:
            if request.method == ['POST', 'PUT']:
                fields.pop('is_published')
                fields.pop('author')
            elif request.method == 'PUT':
                fields.pop('author')
                fields.pop('is_published')
                fields.pop('blog')
        return fields
    
    def create(self, validated_data):
        validated_data['author'] = self.context['user']
        return super().create(validated_data)

    class Meta:
        model = Article
        fields = [
            'id', 'blog', 'name', 'content', 'author',
            'author_name', 'is_published', 'is_archived',
            'created_at', 'has_user_liked', 'article_comments',
        ]
        read_only_fields = ('blog', )


class ArticleCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'

# class CommentSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Comment
#         fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'
