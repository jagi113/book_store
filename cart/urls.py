from django.urls import path, include
from cart import views

app_name = "cart"

urlpatterns = [
    path("add/<str:pk>", views.add_to_cart, name="add_to_cart"),
    path("remove/<str:pk>", views.remove_from_cart, name="remove_from_cart"),
    path("summary", views.cart_summary, name="cart_summary"),
]
