from relationship_app.models import Author, Book, Library, Librarian

# 1. Query all books by a specific author
def get_books_by_author(author_name):
    return Book.objects.filter(author__name=author_name)


# 2. List all books in a library
def get_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        return library.books.all()
    except Library.DoesNotExist:
        return []


# 3. Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        return Librarian.objects.get(library=library)
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None


# Example usage
if __name__ == "__main__":
    # Replace with actual names in your DB
    author_books = get_books_by_author("J.K. Rowling")
    print("Books by J.K. Rowling:", [book.title for book in author_books])

    library_books = get_books_in_library("Central Library")
    print("Books in Central Library:", [book.title for book in library_books])

    librarian = get_librarian_for_library("Central Library")
    print("Librarian for Central Library:", librarian.name if librarian else "Not found")