from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from cart.cart import Cart
from books.models import Book
from cart.forms import CartAddProductForm


# Create your views here.
@require_POST
def add_to_cart(request, pk):
    cart = Cart(request)
    book = get_object_or_404(Book, id=pk)

    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            book=book,
            quantity=cd["quantity"],
            override=cd["override"],
        )
    current_url = request.POST.get("current_url", "/")
    print(current_url)
    return redirect(current_url)


@require_POST
def remove_from_cart(request, pk):
    cart = Cart(request)
    book = get_object_or_404(Book, id=pk)
    cart.remove(book)
    current_url = request.POST.get("current_url", "/")
    return redirect(current_url)


def cart_summary(request):
    cart = Cart(request)
    return render(request, "cart/cart_summary.html", {"cart": cart})
