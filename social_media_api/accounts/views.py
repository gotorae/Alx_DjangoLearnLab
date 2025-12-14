# accounts/views.py
from rest_framework import generics, permissions, status, viewsets, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import CustomUser

from notifications.utils import create_notification


from .models import CustomUser
from .serializers import RegisterSerializer, UserSerializer

class RegisterCreateAPI(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        # run default create
        response = super().create(request, *args, **kwargs)
        # fetch saved user & issue token
        user = CustomUser.objects.get(email=response.data["email"])
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user": UserSerializer(user).data},
            status=status.HTTP_201_CREATED,
        )

class LoginAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is None:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": UserSerializer(user).data})

class ProfileAPI(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class FollowUserAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id: int):
        target = get_object_or_404(CustomUser, id=user_id)
        if target == request.user:
            return Response({"detail": "You cannot follow yourself."},
                                status=status.HTTP_400_BAD_REQUEST)
        request.user.following.add(target)
        
        create_notification(
            actor=request.user,
            recipient=target,
            verb="followed you",
            target=request.user  # the actor is the target entity here
        )
        return Response({"detail": f"You now follow {target.email}."}, status=status.HTTP_200_OK)

    


class UnfollowUserAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id: int):
        target = get_object_or_404(CustomUser, id=user_id)
        if target == request.user:
            return Response({"detail": "You cannot unfollow yourself."},
                            status=status.HTTP_400_BAD_REQUEST)
        request.user.following.remove(target)
        return Response({"detail": f"You no longer follow {target.email}."},
                        status=status.HTTP_200_OK)



from rest_framework import generics
from .serializers import UserSerializer

class FollowingListAPI(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return self.request.user.following.all()

class FollowersListAPI(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return self.request.user.followers.all()
    






