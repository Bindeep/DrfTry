from django.contrib import admin

from .models.blog import Blog
from .models.articles import Article, Comment

admin.site.register(
    [
        Blog,
        Article,
        Comment,
    ]
)
