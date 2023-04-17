from django.shortcuts import render
from books.models import Book
from django.views.generic import ListView, DetailView

# Create your views here.
from django.http import HttpResponse


class Index(ListView):
    template_name = "index.html"
    model = Book
    context_object_name = "books"

    def get_queryset(self):
        queryset = {
            "latest_books": Book.objects.order_by("-updated_at")[:12],
            "best_deals": Book.objects.order_by("price")[:12],
        }
        return queryset


class Book_detail(DetailView):
    template_name = "books/product_details.html"
    model = Book
    context_object_name = "book"


from django.shortcuts import render, redirect


from django.contrib import messages
from books.utils import searchBooks, paginateBooks
from django.contrib import messages
from django.db import IntegrityError


def list_books(request):
    books, search_query = searchBooks(request)

    custom_range, books = paginateBooks(request, books, 12)

    context = {
        "books": books,
        "search_query": search_query,
        "custom_range": custom_range,
    }
    return render(request, "books/products.html", context)
