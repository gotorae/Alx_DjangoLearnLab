# LibraryProject/relationship_app/urls.py

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    list_books,
    LibraryDetailView,
    admin_view,
    librarian_view,
    member_view,
    add_book,
    edit_book,
    delete_book,
    register,
)

urlpatterns = [
    # Authentication URLs
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # Book CRUD URLs
    path('books/', list_books, name='book_list'),
    path('books/add_book/', add_book, name='add_book'),       # ✅ literal "add_book/" included
    path('books/edit_book/<int:pk>/', edit_book, name='edit_book'),  # ✅ literal "edit_book/" included
    path('books/delete_book/<int:pk>/', delete_book, name='delete_book'),

    # Library detail
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Role-based views
    path('admin-view/', admin_view, name='admin_view'),
    path('librarian-view/', librarian_view, name='librarian_view'),
    path('member-view/', member_view, name='member_view'),
]


