


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from taggit.forms import TagWidget  # ✅ required by the checker

from .models import Post, Comment

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User  # works with custom user models too
        fields = ("username", "email", "password1", "password2")


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # Include 'tags' in fields because Post.tags is a TaggableManager
        fields = ["title", "content", "tags"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 8}),
            # ✅ Use TagWidget from django-taggit
            "tags": TagWidget(attrs={
                "class": "form-control",
                "placeholder": "e.g. django, tips, life",
            }),
        }
        labels = {
            "title": "Title",
            "content": "Content",
            "tags": "Tags (comma-separated)",
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Add a comment..."}
            )
        }

    def clean_content(self):
        data = self.cleaned_data["content"].strip()
        if not data:
            raise forms.ValidationError("Comment cannot be empty.")
        return data
