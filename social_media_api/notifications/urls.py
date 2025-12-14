
from django.urls import path
from .views import NotificationListAPIView, NotificationMarkReadAPIView

urlpatterns = [
    path("", NotificationListAPIView.as_view(), name="notifications_list"),
    path("read/", NotificationMarkReadAPIView.as_view(), name="notifications_mark_read"),
]
