from django.shortcuts import get_object_or_404
from django.db.models import F
from django.db.utils import IntegrityError
from django.http import QueryDict
from rest_framework import viewsets
from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import BlogSerializer, ArticleSerializer, CommentSerializer, LikeSerializer, ArticleCreateSerializer
from ..models.blog import Blog
from ..models.articles import Article, Comment, Like
from .permissions import IsRelatedPerson


class BlogListCreate(ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (IsAuthenticated, )


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request}
    
    # def update(self, request, *args, **kwargs):
    #     user = self.request.user.id
    #     data =  {
    #             'blog': self.kwargs.get('pk'),
    #             'author': user
    #         }
    #     ser_data = request.data.dict()
    #     ser_data.update(data)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=ser_data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)

    def get_permissions(self):
        if self.request.method == 'GET':
            return IsAuthenticated(),
        else:
            return IsAuthenticated(), IsRelatedPerson(),

    # def update(self, request, *args, **kwargs):
    #     import ipdb; ipdb.set_trace()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.filter(blog__id=self.kwargs.get('blog_id'))
        return Article.objects.filter(blog__id=self.kwargs.get('blog_id'), is_archived=False)


class CommentView(CreateAPIView):
    queryset = Comment.objects.filter()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, )

    # def create(self, request, *args, **kwargs):
    #     data = request.data
    #     data.update({
    #         'article_id': self.kwargs.get('pk'),
    #         'commented_by': self.request.user
    #     })
    #     serializer = self.get_serializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return IsAuthenticated(),
    #     else:
    #         return IsAuthenticated(), IsRelatedPerson(),

    def perform_create(self, serializer):
        article_id = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_id)
        serializer.save(article=article)

    def create(self, request, *args, **kwargs):
        request.data.update({
            'commented_by': self.request.user.id
        })
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LikeOrDislikeView(APIView):

    permission_classes = (IsAuthenticated, IsRelatedPerson)

    def post(self, request, *args, **kwargs):
        data = {
            'user': request.user.id,
            'article': kwargs.get('pk')
        }
        try:
            Like.objects.get(**data).delete()
        except Like.DoesNotExist:
            ser = LikeSerializer(data=data)
            if ser.is_valid():
                ser.save()
        return Response()


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'is_superuser': user.is_superuser
        })


class CommentDeleteView(DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated, IsRelatedPerson)
    serializer_class = CommentSerializer


class ArticleCreateView(CreateAPIView):
    queryset = Article.objects.all()
    permission_classes = (IsAuthenticated, )
    serializer_class = ArticleCreateSerializer

    def perform_create(self, serializer):
        blog_id = self.kwargs.get('pk')
        blog = get_object_or_404(Blog, pk=blog_id)
        serializer.save(blog=blog)

    def create(self, request, *args, **kwargs):
        request.data.update({
            'author': self.request.user.id
        })
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
