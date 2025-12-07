

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Post, Comment
from .forms import CustomUserCreationForm, PostForm, CommentForm

# Tag model from django-taggit
from taggit.models import Tag


# ---------------------------
# Auth views
# ---------------------------

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Incorrect username or password. Please try again.")
            return redirect("login")

    return render(request, "blog/login.html")


def logout_user(request):
    logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect("login")


# ---------------------------
# Registration
# ---------------------------

def registration(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    return render(request, "signup.html", {"form": form})


# ---------------------------
# Simple pages
# ---------------------------

def home(request):
    return render(request, "blog/home.html")


def posts(request):
    return render(request, "blog/posts.html")


def profile(request):
    if request.method == "POST":
        request.user.email = request.POST.get("email")
        request.user.save()
        messages.success(request, "Profile updated")
        return redirect("profile")
    return render(request, "blog/profile.html")


# ---------------------------
# Posts CRUD
# ---------------------------

class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.all().order_by("-published_date")


class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("posts-list")


class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("posts-list")


class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("posts-list")


# ---------------------------
# Post detail + comments
# ---------------------------

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.select_related("author").all()
        context["comment_form"] = CommentForm()
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("posts-detail", args=[self.kwargs["post_id"]])


class CommentAuthorRequiredMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        return self.get_object().author == self.request.user


class CommentUpdateView(LoginRequiredMixin, CommentAuthorRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def get_success_url(self):
        return reverse("posts-detail", args=[self.object.post_id])


class CommentDeleteView(LoginRequiredMixin, CommentAuthorRequiredMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def get_success_url(self):
        return reverse("posts-detail", args=[self.object.post_id])


# ---------------------------
# Tag filtering & Search
# ---------------------------

def posts_by_tag(request, tag_slug):
    """
    Show posts that include the given tag (by slug).
    """
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = (
        Post.objects.filter(tags__slug=tag.slug)
        .order_by("-published_date")
        .distinct()
    )
    return render(
        request,
        "blog/post_list.html",
        {"posts": posts, "active_tag": tag},
    )


def search_posts(request):
    """
    GET /search/?q=keyword
    Search title, content, and tag names.
    """
    q = request.GET.get("q", "").strip()
    results = Post.objects.none()
    total = 0
    if q:
        results = (
            Post.objects.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q) |
                Q(tags__name__icontains=q)
            )
            .order_by("-published_date")
            .distinct()
        )
        total = results.count()

    return render(
        request,
        "blog/search_results.html",
        {"query": q, "results": results, "total": total},
    )






class PostByTagListView(ListView):
    model = Post
    template_name = "blog/post_list.html"   # or your template
    context_object_name = "posts"

    def get_queryset(self):
        tag_slug = self.kwargs.get("tag_slug")
        return Post.objects.filter(tags__slug=tag_slug)
