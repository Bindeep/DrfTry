from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Blog(models.Model):
    title = models.CharField('Blog Title', max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        related_name='blogs',
        on_delete=models.DO_NOTHING,
    )
    is_archived = False

    def __str__(self):
        return self.title
    
    def get_name(self):
        return self.author.username
