
from django.contrib import admin
from .models import Book
from .models import CustomerUser

class CustomerUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date_of_birth')
    search_fields = ('name', 'email')
    list_filter = ('name', 'email')

admin.site.register(CustomerUser, CustomerUserAdmin)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('title', 'author')

admin.site.register(Book, BookAdmin)


# Register your models here.
