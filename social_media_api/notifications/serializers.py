
from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor_email = serializers.EmailField(source="actor.email", read_only=True)
    recipient_email = serializers.EmailField(source="recipient.email", read_only=True)
    target_model = serializers.CharField(source="target_content_type.model", read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "actor_email",
            "recipient_email",
            "verb",
            "target_model",
            "target_object_id",
            "is_read",
            "created_at",
        ]
