from rest_framework import routers
from .views import (
    BlogViewSet, ArticleViewSet,
    CommentViewSet, LikeOrDislikeView,
    CommentView
    )
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'blogs', BlogViewSet)
router.register(r'articles', ArticleViewSet)
# router.register(r'(?P<article_id>[0-9+])/comments', CommentViewSet)
router.register(r'comments', CommentViewSet)

# comment = CommentViewSet.as_view()

urlpatterns = [
    path('', include(router.urls)),
    path('article/<int:pk>/like/', LikeOrDislikeView.as_view(), name='like_dislike'),
    path('article/<int:>/comment/', CommentView.as_view(), name='post_comment'),
]