from django.contrib import admin

from products.models import Categories, Products


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "quantity", "price"]
    list_editable = ["price", "quantity",]
    search_fields = ["name", "description"]
    list_filter = ["quantity", "category"]
    fields = [
        "name",
        "category",
        "slug",
        "description",
        "image",
        "price",
        "quantity",
    ]

