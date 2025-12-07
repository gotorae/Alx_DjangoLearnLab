
from django.contrib import admin
from .models import Post, Comment

# If using django-taggit, you don't need to register Tag manually.
# If using custom Tag model, uncomment the next line:
# from .models import Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_date")
    list_filter = ("author", "published_date")
    search_fields = ("title", "content")
    date_hierarchy = "published_date"
    ordering = ("-published_date",)
    # If using django-taggit, tags will appear automatically in the form.
    # If using custom Tag model, you can add 'tags' to fields below:
    fields = ("title", "content", "author", "tags")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "created_at", "updated_at")
    list_filter = ("author", "created_at")
    search_fields = ("content",)
    ordering = ("-created_at",)


# If using custom Tag model:
# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     list_display = ("name", "slug")
#     search_fields = ("name",)

