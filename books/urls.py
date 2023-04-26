from django.urls import path, include
from books import views

app_name = "books"

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("list", views.list_books, name="book_list"),
    path("detail/<str:pk>", views.Book_detail.as_view(), name="book_detail"),
]
