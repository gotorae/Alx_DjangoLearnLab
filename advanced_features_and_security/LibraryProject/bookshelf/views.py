from django.shortcuts import render, redirect
from django.http import HttpResponse

def index(request): return HttpResponse("Welcome to my book app.")


from .models import Book
from django.db.models import Q

def search_books(request):
    query = request.GET.get('q', '')
    # Safe ORM query instead of raw SQL
    books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    return render(request, 'bookshelf/book_list.html', {'books': books})


from .forms import ExampleForm

def create_book(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})


from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404
from .models import Book

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    # Logic for creating a book
    pass

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # Logic for editing a book
    pass

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return render(request, 'bookshelf/book_deleted.html')



# Create your views here.
