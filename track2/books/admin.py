from django.contrib import admin

from .models import Book, Rental


# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title','author','stock']

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ['rental_book','rental_user','rental_date','return_date']


