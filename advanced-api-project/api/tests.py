from django.test import TestCase
from django.urls import reverse
from .models import Author, Book
from rest_framework.test import APIClient
from rest_framework import status


class BookModelTest(TestCase):
    def test_book_model_create(self):
        author = Author.objects.create(name="Tsitsi Dangarembga")

        book = Book.objects.create(
            title="Nervous Conditions",
            publication_year=2002,
            author=author
        )

        self.assertEqual(book.title, "Nervous Conditions")
        self.assertEqual(book.publication_year, 2002)
        self.assertEqual(book.author.name, "Tsitsi Dangarembga")


class BookAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(name="John Wilson")

    def test_create_book_api(self):
        url = reverse("book-create")

        data = {
            "title": "Macbeth",
            "publication_year": 1991,
            "author": self.author.id
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.first().title, "Macbeth")

    def test_list_books_api(self):
        Book.objects.create(
            title="Book A",
            publication_year=2000,
            author=self.author
        )

        url = reverse("book-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_book_detail_api(self):
        book = Book.objects.create(
            title="Detail Test",
            publication_year=2005,
            author=self.author
        )

        url = reverse("book-detail", kwargs={"pk": book.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Detail Test")

    def test_book_update_api(self):
        book = Book.objects.create(
            title="Old Title",
            publication_year=2010,
            author=self.author
        )

        url = reverse("book-update", kwargs={"pk": book.id})

        data = {
            "title": "New Title",
            "publication_year": 2015,
            "author": self.author.id
        }

        response = self.client.put(url, data, format="json")
        updated_book = Book.objects.get(id=book.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_book.title, "New Title")

    def test_book_delete_api(self):
        book = Book.objects.create(
            title="To Delete",
            publication_year=2018,
            author=self.author
        )

        url = reverse("book-delete", kwargs={"pk": book.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)



# Create your tests here.
