from django.test import TestCase
from .models import auth, Book
from .serializer import AuthorSerializer, BookSerializer
from django.urls import reverse


class BookModelTest(TestCase):

    def test_book_create(self):
        reg = Book.objects.create(
            title = "nervouse condition",
            publication_year = '10/02/2002',
            author = 'tsitsi dangarembgwa'
        )

        self.assertEqual(reg.title, 'nervouse condition')
        self.assertEqual(reg.author, 'tsitsi dangarembgwa')

# Create your tests here.
