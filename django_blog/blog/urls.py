
from django.urls import path
from .views import home, login_user, logout_user, registration, profile
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    CommentCreateView, CommentUpdateView, CommentDeleteView,
    posts_by_tag, search_posts,
)

urlpatterns = [
    # Core pages
    path("", home, name="home"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("register/", registration, name="register"),
    path("profile/", profile, name="profile"),

    # Posts list + CRUD
    path("posts/", PostListView.as_view(), name="posts-list"),
    path("posts/new/", PostCreateView.as_view(), name="posts-create"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="posts-detail"),
    path("posts/<int:pk>/edit/", PostUpdateView.as_view(), name="posts-update"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="posts-delete"),

    # Comments
    path("posts/<int:post_id>/comments/new/", CommentCreateView.as_view(), name="comment-create"),
    path("comments/<int:pk>/edit/", CommentUpdateView.as_view(), name="comment-update"),
    path("comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),

    # NEW: Tag filtering and Search
    path("tags/<slug:tag_slug>/", posts_by_tag, name="posts-by-tag"),
    path("search/", search_posts, name="post-search"),
]

