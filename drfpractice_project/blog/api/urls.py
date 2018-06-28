from rest_framework import routers
from .views import BlogViewSet, ArticleViewSet, CommentViewSet, increase_like
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'blogs', BlogViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('articles/<int:id>/uplike/', increase_like, name='increase_like'),
]