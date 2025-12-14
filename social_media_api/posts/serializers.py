# posts/serializers.py
from rest_framework import serializers
from .models import Post, Comment, Like

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Post
        fields = ["id", "author", "title", "content", "created_at", "updated_at", "latitude", "longitude"]
        read_only_fields = ["author", "created_at", "updated_at"]

    def create(self, validated_data):
        return Post.objects.create(author=self.context["request"].user, **validated_data)

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Comment
        fields = ["id", "post", "author", "content", "created_at", "updated_at", "latitude", "longitude"]
        read_only_fields = ["author", "created_at", "updated_at"]

    def create(self, validated_data):
        return Comment.objects.create(author=self.context["request"].user, **validated_data)




class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)
    liked = serializers.SerializerMethodField()  # whether current user liked this post

    class Meta:
        model = Post
        fields = [
            "id","author","title","content",
            "created_at","updated_at",
            "latitude","longitude",
            "likes_count","liked",
        ]
        read_only_fields = ["author","created_at","updated_at","likes_count","liked"]

    def get_liked(self, obj):
        user = self.context["request"].user
        if not user.is_authenticated:
            return False
        return obj.likes.filter(user=user).exists()

    def create(self, validated_data):
        return Post.objects.create(author=self.context["request"].user, **validated_data)

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Comment
        fields = ["id","post","author","content","created_at","updated_at","latitude","longitude"]
        read_only_fields = ["author","created_at","updated_at"]

    def create(self, validated_data):
        return Comment.objects.create(author=self.context["request"].user, **validated_data)
