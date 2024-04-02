from django.urls import path

from cart import views

app_name = "cart"

urlpatterns = [
    path("add_cart/", views.add_cart, name="add_cart"),
    path("change_cart/", views.change_cart, name="change_cart"),
    path("delete_cart/", views.delete_cart, name="delete_cart"),
]