from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import Author, Book


class BookAPITestCase(APITestCase):

    def setUp(self):
        self.author = Author.objects.create(name="John Wilson")

    def test_create_book(self):
        url = reverse("book-create")
        data = {
            "title": "Macbeth",
            "publication_year": 1991,
            "author": self.author.id
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)

    def test_list_books(self):
        Book.objects.create(
            title="Book A",
            publication_year=2000,
            author=self.author
        )

        url = reverse("book-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_book_detail(self):
        book = Book.objects.create(
            title="Detail Book",
            publication_year=2005,
            author=self.author
        )

        url = reverse("book-detail", kwargs={"pk": book.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Detail Book")

    def test_update_book(self):
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
        book.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(book.title, "New Title")

    def test_delete_book(self):
        book = Book.objects.create(
            title="Delete Book",
            publication_year=2018,
            author=self.author
        )

        url = reverse("book-delete", kwargs={"pk": book.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
