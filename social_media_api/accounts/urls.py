from django.urls import path
from .views import (RegisterCreateAPI, LoginAPI, ProfileAPI, FollowersListAPI, UnfollowUserAPI, FollowUserAPI
                    )

urlpatterns = [
    path("register/", RegisterCreateAPI.as_view(), name="register"),
    path("login/", LoginAPI.as_view(), name="login"),
    path("profile/", ProfileAPI.as_view(), name="profile"),
    
    path("follow/<int:user_id>/",   FollowUserAPI.as_view(),   name="follow_user"),
    path("unfollow/<int:user_id>/", UnfollowUserAPI.as_view(), name="unfollow_user"),

    

]
