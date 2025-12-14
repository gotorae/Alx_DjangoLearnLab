# posts/urls.py


from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import PostViewSet, CommentViewSet, FeedAPIView, LikePostAPI, UnlikePostAPI

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = router.urls + [
    path("feed/", FeedAPIView.as_view(), name="feed"),
    path("posts/<int:pk>/like/", LikePostAPI.as_view(), name="post_like"),
    path("posts/<int:pk>/unlike/", UnlikePostAPI.as_view(), name="post_unlike"),
]


