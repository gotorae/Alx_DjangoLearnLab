import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# --- Sample Queries ---

# 1. Query all books by a specific author (two ways)

author_name = "John Doe"

# Way 1: Using a direct filter on author name
books_by_author = Book.objects.filter(author__name=author_name)
print(f"Books by {author_name} (filter by name): {[book.title for book in books_by_author]}")

# Way 2: Get the Author object first, then filter
author = Author.objects.get(name=author_name)
books_by_author_2 = Book.objects.filter(author=author)
print(f"Books by {author_name} (filter by object): {[book.title for book in books_by_author_2]}")


# 2. List all books in a library

library_name = "Central Library"
try:
    library = Library.objects.get(name=library_name)
    print(f"Books in {library_name}: {[book.title for book in library.books.all()]}")
except Library.DoesNotExist:
    print(f"Library '{library_name}' not found.")


# 3. Retrieve the librarian for a library (two ways)

# Way 1: Using the reverse relationship from Library
try:
    librarian = library.librarian
    print(f"Librarian for {library_name} (reverse relation): {librarian.name}")
except Librarian.DoesNotExist:
    print(f"No librarian assigned to '{library_name}'.")

# Way 2: Using a direct query on Librarian
try:
    librarian_direct = Librarian.objects.get(library=library)
    print(f"Librarian for {library_name} (direct query): {librarian_direct.name}")
except Librarian.DoesNotExist:
    print(f"No librarian assigned to '{library_name}'.")
