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
    is_archived = False
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def get_author(self):
        return self.author.username


class Comment(models.Model):
    article = models.ForeignKey(
        Article, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    commented_by = models.ForeignKey(
        User, related_name='comments', on_delete=models.DO_NOTHING)
    commented_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title[:30]} commented by {self.commented_by}'


class Like(models.Model):
    article = models.ForeignKey(Article, related_name='article_likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_likes', on_delete=models.CASCADE)

    def __str__(self):
        return f'liked {self.article} by {self.user.username}'
    
    class Meta:
        unique_together = ('user', 'article')