from django.urls import path, include
from books import views

app_name = "books"

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("list", views.list_books, name="book_list"),
    path("detail/<str:pk>", views.Book_detail.as_view(), name="book_detail"),
    path("add_to_cart", views.add_to_cart, name="add_to_cart"),
    path("cart", views.cart_summary, name="cart_summary"),
]
