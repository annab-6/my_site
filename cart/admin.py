from django.contrib import admin

from cart.models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["display_user", "display_product", "quantity", "timestamp",]
    list_filter = ["timestamp", "user", "product__name",]


    def display_user(self, obj):
        if obj.user:
            return str(obj.user)
        return "Anonymous user"


    def display_product(self, obj):
        return str(obj.product.name)


class CartTabAdmin(admin.TabularInline):
    model = Cart
    fields = "product", "quantity", "timestamp"
    search_fields = "product", "quantity", "timestamp"
    readonly_fields = ("timestamp",)
    extra = 1
