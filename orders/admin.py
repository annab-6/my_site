from django.contrib import admin

from orders.models import Order, OrderItem


class OrderItemTabularAdmin(admin.TabularInline):
    """
    : Это класс для представления элементов заказа в виде табличной формы в интерфейсе администратора
    """
    model = OrderItem
    fields = ("product", "name", "price", "quantity")
    search_fields = ("product__name", "name")
    extra = 0


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """

    Это класс для настройки отображения элементов заказа в списке администратора.
    Он определяет, какие поля будут отображаться в списке, а также поля для поиска
    ."""
    list_display = ("order", "product", "name", "price", "quantity")
    search_fields = ("order__id", "product__name", "name")



class OrderTabularAdmin(admin.TabularInline):
    """
    Этот класс определяет представление заказов в виде табличной формы в интерфейсе администратора.
    Он также определяет настройки поиска и только для чтения поле времени создания.

    """
    model = Order
    fields = ("requires_delivery", "status", "payment_on_get", "is_paid", "timestamp")
    search_fields = ("requires_delivery", "payment_on_get", "is_paid", "timestamp")
    readonly_fields = ("timestamp",)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Это класс для настройки отображения заказов в списке администратора.
     Он определяет, какие поля будут отображаться в списке, а также поля для поиска,
      фильтры и встраиваемые элементы для отображения элементов заказа.
      """
    list_display = ("id", "user", "requires_delivery", "status", "payment_on_get", "is_paid", "timestamp")
    search_fields = ("id",)
    readonly_fields = ("timestamp",)
    list_filter = ("requires_delivery", "status", "payment_on_get", "is_paid")
    inlines = (OrderItemTabularAdmin,)
