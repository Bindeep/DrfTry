from django.urls import path, include
from rest_framework import routers
from .views import (
    BlogListCreate, ArticleViewSet, LikeOrDislikeView,
    CommentView, CustomAuthToken, CommentDeleteView,
    ArticleCreateView
    )


app_name = 'blog'

router = routers.DefaultRouter()
router.register(r'articles', ArticleViewSet)

blog_list_create = BlogListCreate.as_view()

urlpatterns = [
    path('blogs/', blog_list_create, name='blog_list'),
    path('article/<int:pk>/like/', LikeOrDislikeView.as_view(), name='like_dislike'),
    path('article/<int:pk>/comment/', CommentView.as_view(), name='post_comment'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='delete_comment'),
    path('blog/<int:pk>/article/create/', ArticleCreateView.as_view(), name='create_article'),
    path('blog/<int:blog_id>/', include(router.urls))
]


urlpatterns += [
    path('api-token-auth/', CustomAuthToken.as_view())
]
