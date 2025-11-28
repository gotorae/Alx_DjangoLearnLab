from django.db import models


class Author(models.Model):
    
        """
        Represents a book author.
        - name: the author's display name.
        """
        name = models.CharField(max_length=250)

        def __str__(self):
              return self.name


class Book(models.Model):

    
    """
        Represents a book written by an Author.
        - title: human-readable title of the book.
        - publication_year: 4-digit integer; we'll validate it's not in the future.
        - author: FK to Author (one author -> many books).
        related_name='books' lets us access author.books in serializers.
        """


    title = models.CharField(max_length=250)
    publication_year = models.IntegerField(max_length=4)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='writer')

    def _str__(self):
          return f"{self.title} ({self.publication_year})"

# Create your models here.
