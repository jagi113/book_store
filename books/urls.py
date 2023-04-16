from django.urls import path, include
from books import views

app_name='books'

urlpatterns = [
    path('', views.BookList.as_view(), name = "book_list"), 
]