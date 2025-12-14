# posts/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["author"]  # filter by author id: /posts/?author=1
    search_fields = ["title", "content", "author__username", "author__email"]
    ordering_fields = ["created_at", "updated_at", "title"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("author", "post")
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["post", "author"]  # /comments/?post=5&author=1
    search_fields = ["content", "author__username", "author__email", "post__title"]
    ordering_fields = ["created_at", "updated_at"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)






class FeedAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # IDs of users current user follows
        following_ids = user.following.values_list("id", flat=True)
        return (Post.objects
                    .select_related("author")
                    .filter(author_id__in=following_ids)
                    .order_by("-created_at"))




from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

# Notifications utility
from notifications.utils import create_notification

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["author"]
    search_fields = ["title", "content", "author__username", "author__email"]
    ordering_fields = ["created_at", "updated_at", "title"]

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        # Optional: notify followers that the author posted (not required by brief)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("author", "post")
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["post", "author"]
    search_fields = ["content", "author__username", "author__email", "post__title"]
    ordering_fields = ["created_at", "updated_at"]

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        post = comment.post
        # Notify the post author (skip self-notify)
        if post.author != self.request.user:
            create_notification(
                actor=self.request.user,
                recipient=post.author,
                verb="commented on your post",
                target=post
            )

class LikePostAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk: int):
        post = get_object_or_404(Post, pk=pk)
        # prevent duplicate like
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            return Response({"detail": "Already liked"}, status=status.HTTP_200_OK)

        # notify post author (skip self-notify)
        if post.author != request.user:
            from notifications.utils import create_notification
            create_notification(
                actor=request.user,
                recipient=post.author,
                verb="liked your post",
                target=post
            )
        return Response({"detail": "Liked"}, status=status.HTTP_201_CREATED)

class UnlikePostAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk: int):
        post = get_object_or_404(Post, pk=pk)
        deleted, _ = Like.objects.filter(post=post, user=request.user).delete()
        if deleted == 0:
            return Response({"detail": "Not liked yet"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Unliked"}, status=status.HTTP_200_OK)
    


class PostAPIview(generics.ListAPIView):
    model = Post.objects.all()
    serializer_class = PostSerializer


class CommentAPIview(generics.ListAPIView):
    model = Comment.objects.all()
    serializer_class = CommentSerializer


