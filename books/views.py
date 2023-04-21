from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views.generic import ListView, DetailView, View
from django.urls import reverse
import operator

from books.models import Book
from books.utils import searchBooks, paginateBooks, getRandomBooks

# Create your views here.


class Index(ListView):
    template_name = "index.html"
    model = Book
    context_object_name = "books"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        cart = request.session.get("cart")
        context["cart"] = cart
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
        request = self.request
        cart = request.session.get("cart")
        context["cart"] = cart
        return context


def list_books(request):
    cart = request.session.get("cart")
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


def add_to_cart(request):
    try:
        url = request.META.get("HTTP_REFERER")
    except:
        url = None

    if request.method == "POST":
        book_id = request.POST["buy_id"]
        cart = request.session.get("cart")
        if cart:
            request.session["cart"] = cart.append(book_id)
        else:
            request.session["cart"] = [
                book_id,
            ]
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


def cart_summary(request):
    cart = request.session.get("cart")
    print(cart)
    if not cart:
        return render(request, "books/cart_summary.html", {cart: None})
    purchasing_books = [Book.objects.get(pk=book) for book in cart]

    price = round(float(sum([book.price for book in purchasing_books])), 2)
    no_tax_price = round(
        sum([(float(book.price) / 1.2) for book in purchasing_books]), 2
    )
    tax = round(price - no_tax_price, 2)
    context = {
        "cart": purchasing_books,
        "no_tax_price": no_tax_price,
        "tax": tax,
        "price": price,
    }
    return render(request, "books/cart_summary.html", context)
