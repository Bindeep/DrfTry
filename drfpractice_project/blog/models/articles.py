from django.db import models
from django.contrib.auth import get_user_model
from .blog import Blog

User = get_user_model()

class Article(models.Model):
    name = models.CharField('Name of an Article', max_length=255)
    content = models.TextField()
    blog = models.ForeignKey(Blog, related_name='articles', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='related_articles', on_delete=models.DO_NOTHING)
    is_published = models.BooleanField(default=False)
    like = models.PositiveIntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    @property
    def get_author(self):
        return self.author.username


class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    title = models.TextField()
    commented_by = models.ForeignKey(User, related_name='comments', on_delete=models.DO_NOTHING)
    commented_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title[:30]} commented by {self.commented_by}'