import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# --- Sample Queries ---

# 1. Query all books by a specific author
author_name = "John Doe"
# Get the author object first
author = Author.objects.get(name=author_name)
# Filter books by author object
books_by_author = Book.objects.filter(author=author)
print(f"Books by {author_name}: {[book.title for book in books_by_author]}")

# 2. List all books in a library
library_name = "Central Library"
try:
    library = Library.objects.get(name=library_name)
    print(f"Books in {library_name}: {[book.title for book in library.books.all()]}")
except Library.DoesNotExist:
    print(f"Library '{library_name}' not found.")

# 3. Retrieve the librarian for a library using direct query
try:
    librarian = Librarian.objects.get(library=library)  # <-- required string
    print(f"Librarian for {library_name}: {librarian.name}")
except Librarian.DoesNotExist:
    print(f"No librarian assigned to '{library_name}'.")

