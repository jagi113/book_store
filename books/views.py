from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views.generic import ListView, DetailView, View
from django.urls import reverse
import operator

from books.models import Book
from cart.cart import Cart
from books.utils import searchBooks, paginateBooks, getRandomBooks

# Create your views here.


class Index(ListView):
    template_name = "index.html"
    model = Book
    context_object_name = "books"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"] = Cart(self.request)
        return context

    def get_queryset(self):
        queryset = {
            "carousel_content": getRandomBooks(4),
            "latest_books": Book.objects.order_by("-updated_at")[:12],
            "best_deals": Book.objects.order_by("price")[:12],
        }
        return queryset


class Book_detail(DetailView):
    template_name = "books/product_details.html"
    model = Book
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart"] = Cart(self.request)
        return context


def list_books(request):
    cart = Cart(request)
    books, search_query = searchBooks(request)

    order = "title"
    if request.GET.get("order"):
        order = request.GET.get("order")

    sorted_books = books.order_by(order)

    custom_range, book_list = paginateBooks(request, sorted_books, 12)

    context = {
        "books": book_list,
        "search_query": search_query,
        "custom_range": custom_range,
        "cart": cart,
    }
    return render(request, "books/products.html", context)
