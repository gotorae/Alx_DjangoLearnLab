from django.contrib import admin
from .models import CustomerUser



class CustomerUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date_of_birth')
    search_fields = ('name', 'email')
    list_filter = ('name', 'email')

admin.site.register(CustomerUser, CustomerUserAdmin)

# Register your models here.
