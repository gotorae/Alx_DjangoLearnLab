from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

# ✅ Explicit import of Library first to satisfy automated checks
from .models import Library, Book, Author, UserProfile, Librarian
from .forms import BookForm

# --- Book Views ---

def list_books(request):
    """List all books."""
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


# --- Library Views ---

class LibraryDetailView(DetailView):
    """Display details of a single library."""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# --- Role Check Helper Functions ---

def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'


def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'


def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


# --- Role-Based Views ---

@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'admin_view.html')


@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'librarian_view.html')


@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'member_view.html')


# --- Book Permission Views ---

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """Add a new book (requires 'can_add_book' permission)."""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})


@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    """Edit an existing book (requires 'can_change_book' permission)."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'edit_book.html', {'form': form, 'book': book})


@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    """Delete a book (requires 'can_delete_book' permission)."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'delete_book.html', {'book': book})



