from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from pages.api.serializers import PostCreateSerializer, PostSerializer
from pages.models import Post


class PostCreateAPIView(CreateAPIView):
    serializer_class = PostCreateSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRetrieveAPIView(RetrieveAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostUpdateDestroyAPIView(UpdateAPIView, DestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


class PostListAPIView(ListAPIView):
    pagination_class = LimitOffsetPagination
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostLikeAPIView(APIView):

    def get(self, request, pk):
        obj = get_object_or_404(Post, pk=pk)
        user = self.request.user
        if user in obj.likes.all():
            obj.likes.remove(user)
        else:
            obj.likes.add(user)
        return Response(status=status.HTTP_200_OK)
