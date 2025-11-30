from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from api.models import Author, Book


class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create a test user for authenticated views
        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )

        # Create an author
        self.author = Author.objects.create(name="John Wilson")

    def test_create_book(self):
        url = reverse("book-create")

        data = {
            "title": "Macbeth",
            "publication_year": 1991,
            "author": self.author.id
        }

        response = self.client.post(url, data, format="json")

        # Use response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Macbeth")

    def test_list_books(self):
        Book.objects.create(
            title="Book A",
            publication_year=2000,
            author=self.author
        )

        url = reverse("book-list")
        response = self.client.get(url)

        # Use response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Book A")

    def test_book_detail_authenticated(self):
        self.client.login(username="testuser", password="password123")

        book = Book.objects.create(
            title="Detail Book",
            publication_year=2005,
            author=self.author
        )

        url = reverse("book-detail", kwargs={"pk": book.id})
        response = self.client.get(url)

        # Use response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Detail Book")

    def test_update_book_authenticated(self):
        self.client.login(username="testuser", password="password123")

        book = Book.objects.create(
            title="Old Title",
            publication_year=2010,
            author=self.author
        )

        url = reverse("book-update", kwargs={"pk": book.id})

        data = {
            "title": "New Title",
            "publication_year": 2022,
            "author": self.author.id
        }

        response = self.client.put(url, data, format="json")

        # Use response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "New Title")

    def test_delete_book_authenticated(self):
        self.client.login(username="testuser", password="password123")

        book = Book.objects.create(
            title="Delete Me",
            publication_year=2018,
            author=self.author
        )

        url = reverse("book-delete", kwargs={"pk": book.id})
        response = self.client.delete(url)

        # Delete API returns no content, but we check with response.data gracefully
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)
