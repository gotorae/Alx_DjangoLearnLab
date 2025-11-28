from rest_framework import serializers
from .models import Author, Book
from datetime import date

#book serializer
class BookSerializer(serializers.ModelSerializer):

    
    """
        Serializes Book instances.

        Custom validation:
        - publication_year must not be in the future.
        """


    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author']

#author serializer
class AuthorSerializer(serializers.ModelSerializer):
    
    
    """
        Serializes Author instances.

        Nested relationship:
        - `books`: a nested, read-only list of the author's books using BookSerializer.
        This uses the `related_name='books'` defined on Book.author.
        """

    
    
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']

# validate the publication year
    def validate_publication_year(self, value):
        current_date = date.today().year
        if value > current_date:
            raise serializers.ValidationError("publication date cannot be in the future")
        return value
    
