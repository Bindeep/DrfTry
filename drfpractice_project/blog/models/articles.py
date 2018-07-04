from django.db import models
from django.contrib.auth import get_user_model
from .blog import Blog

User = get_user_model()


class Article(models.Model):
    name = models.CharField('Name of an Article', max_length=255)
    content = models.TextField()
    blog = models.ForeignKey(
        Blog, related_name='articles', on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, related_name='related_articles', on_delete=models.DO_NOTHING)
    is_published = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def author_name(self):
        return self.author.username


class Comment(models.Model):
    article = models.ForeignKey(
        Article, related_name='article_comments', on_delete=models.CASCADE)
    content = models.TextField()
    commented_by = models.ForeignKey(
        User, related_name='user_comments', on_delete=models.DO_NOTHING)
    commented_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.content[:30]} commented by {self.commented_by}'

    @property
    def commented_by_name(self):
        return self.commented_by.username


class Like(models.Model):
    article = models.ForeignKey(Article, related_name='article_likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_likes', on_delete=models.CASCADE)

    def __str__(self):
        return f'liked {self.article} by {self.user.username}'
    
    class Meta:
        unique_together = ('user', 'article')