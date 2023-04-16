from django.shortcuts import render
from books.models import Book
from django.views.generic import ListView

# Create your views here.
from django.http import HttpResponse

class BookList(ListView):
    template_name = "books/book_list.html"
    model = Book
    context_object_name = "books"

