
from django.contrib.contenttypes.models import ContentType
from .models import Notification

def create_notification(actor, recipient, verb, target=None):
    n = Notification(actor=actor, recipient=recipient, verb=verb)
    if target is not None:
        n.target_content_type = ContentType.objects.get_for_model(target.__class__)
        n.target_object_id = target.pk
    n.save()
    return n
