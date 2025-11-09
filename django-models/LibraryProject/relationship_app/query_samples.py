import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# --- Sample Queries ---

# Define author name first
author_name = "John Doe"

# Two-step approach
author = Author.objects.get(name=author_name)
books_by_author = Book.objects.filter(author=author)

# OR single-line approach (you already have this below)
# books_by_author = Book.objects.filter(author__name=author_name)

print(f"Books by {author_name}: {[book.title for book in books_by_author]}")

# List all books in a library
library_name = "Central Library"
try:
    library = Library.objects.get(name=library_name)
    print(f"Books in {library_name}: {[book.title for book in library.books.all()]}")
except Library.DoesNotExist:
    print(f"Library '{library_name}' not found.")

# Retrieve the librarian for a library
try:
    librarian = library.librarian
    print(f"Librarian for {library_name}: {librarian.name}")
except Exception:
    print(f"No librarian assigned to '{library_name}'.")
