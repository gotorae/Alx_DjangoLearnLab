from django.shortcuts import render
from rest_framework import generics, viewsets, filters, permissions
from .serializers import BookSerializer, AuthorSerializer
from .models import Author, Book



class BookListView(generics.ListAPIView):
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['tiltle', 'author_name']
    ordering_fields = ['publication_year', 'title']
    ordering = ['title']

    
    def get_queryset(self):
        qs = super().get_queryset()
        min_year = self.request.query_params.get('min_year')
        max_year = self.request.query_params.get('max_year')
        if min_year:
            qs = qs.filter(publication_year__gte=min_year)
        if max_year:
            qs = qs.filter(publication_year__lte=max_year)
        return qs


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    
    def perform_create(self, serializer):
        serializer.save()


class BookAPIView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

   


class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes= [permissions.IsAuthenticated]
    lookup_field = 'pk'


class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field ='pk'

        





# Create your views here.
