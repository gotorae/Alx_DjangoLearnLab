from django.urls import path
from .views import (
    BookCreateView,
    BookDeleteView,
    BookDetailView,
    BookListView,
    BookUpdateView,
)


urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),                     # ListView
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),        # DetailView
    path('books/create/', BookCreateView.as_view(), name='book-create'),          # CreateView
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'), # UpdateView
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'), # DeleteView
]
