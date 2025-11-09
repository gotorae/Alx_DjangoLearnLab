import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# --- Sample Queries ---

# 1. Query all books by a specific author
author_name = "John Doe"
try:
    author = Author.objects.get(name=author_name)
    books_by_author = Book.objects.filter(author=author)
    print(f"Books by {author_name}: {[book.title for book in books_by_author]}")
except Author.DoesNotExist:
    print(f"No author found with name '{author_name}'.")

# 2. List all books in a library
library_name = "Central Library"
try:
    library = Library.objects.get(name=library_name)
    print(f"Books in {library_name}: {[book.title for book in library.books.all()]}")
except Library.DoesNotExist:
    print(f"Library '{library_name}' not found.")

# 3. Retrieve librarians for a library
try:
    librarians = library.librarians.all()
    if librarians.exists():
        print(f"Librarians for {library_name}: {[librarian.user.username for librarian in librarians]}")
    else:
        print(f"No librarians assigned to '{library_name}'.")
except NameError:
    # library variable not defined if Library.DoesNotExist above
    pass
