# Create Operation
```python
from bookshelf.models import Book
book = Book.objects.create(title='1984', author='George Orwell', publication_year=1949)
book  # Output: <Book: 1984>


# Retrieve 
retrieve_book = Book.objects.all()

# Update
book.title = 'Nineteen Eighty-Four'

# delete
book.title = 'Nineteen Eighty-Four'