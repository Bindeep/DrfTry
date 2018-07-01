from rest_framework import permissions
from ..models.blog import Blog
from ..models.articles import Article, Comment, Like

class IsRelatedPerson(permissions.BasePermission):
    """
    Permission Check for if the user is author.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user.is_superuser:
            if isinstance(obj, Article):
                return obj.author == request.user
            elif isinstance(obj, Comment):
                return request.user in (obj.commented_by, obj.article.author,)
            elif isinstance(obj, Like):
                return obj.user == request.user
        return True
        