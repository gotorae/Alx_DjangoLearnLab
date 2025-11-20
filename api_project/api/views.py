from django.shortcuts import render, redirect
from rest_framework import generics, viewsets
from .serializers import BookSerializer
from .models import Book
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from .serializers import  UserSerializer
from .permissions import IsOwner



class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class AdminOnlyViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer()
    permission_classes= [IsAdminUser]


permission_classes = [IsAuthenticated, IsOwner]


# Create your views here.
