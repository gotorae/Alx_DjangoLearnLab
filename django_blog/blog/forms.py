

# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import Post, Comment

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User  # works with custom user model via get_user_model()
        fields = ("username", "email", "password1", "password2")


class PostForm(forms.ModelForm):
    # Expose a simple text field for comma-separated tags
    tags = forms.CharField(
        required=False,
        help_text="Comma-separated tags (e.g., django, tips, life).",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "django, tips, life"}
        ),
        label="Tags",
    )

    class Meta:
        model = Post
        fields = ["title", "content"]  # author is set in the view; tags handled separately
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 8}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prepopulate with existing tags as comma-separated text
        if self.instance.pk:
            self.fields["tags"].initial = ", ".join(self.instance.tags.names())

    def save(self, commit=True):
        post = super().save(commit=commit)
        # Parse and set tags via taggit (auto-creates missing tags)
        raw = self.cleaned_data.get("tags", "")
        names = [t.strip() for t in raw.split(",") if t.strip()]
        post.tags.set(names)
        return post


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
