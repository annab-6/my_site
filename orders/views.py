from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect, render
from cart.models import Cart

from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem
from django.contrib.auth.decorators import login_required


@login_required
def create_order(request):
    """предназначена для обработки создания заказа пользователем."""
    if request.method == 'POST':
        # Создаёт экземпляр формы заказа на основе данных из POST запроса.
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():  # Либо все операции внутри блока будут выполнены успешно, либо ни одна из них.
                    user = request.user  # Получаем пользователя, который отправил запрос.
                    cart_items = Cart.objects.filter(user=user)  # Получаем все товары в корзине этого пользователя.

                    if cart_items.exists():

                        order = Order.objects.create(     # создается заказ с использованием данных из формы и пользователя.
                            user=user,
                            phone_number=form.cleaned_data['phone_number'],
                            requires_delivery=form.cleaned_data['requires_delivery'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            payment_on_get=form.cleaned_data['payment_on_get'],
                        )

                        for cart_item in cart_items:
                            product = cart_item.product
                            name = cart_item.product.name
                            price = cart_item.product.sell_price()
                            quantity = cart_item.quantity

                            if product.quantity < quantity:
                                raise ValidationError(f'Insufficient quantity of products {name} in stock\
                                                           In stock - {product.quantity}')
                            # создается обьект для каждого товара с данными о нем
                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                            )
                            product.quantity -= quantity   #уменьшает кол-во товара в наличии
                            product.save()

                        # Очистить корзину юзера после создания заказа
                        cart_items.delete()

                        messages.success(request, 'Order is processed!')
                        return redirect('users:profile')
            except ValidationError as e:
                messages.error(request, str(e))
                return redirect('cart:create_order')
    else:
        initial = {
            'first_name': request.user.first_name,     # начальные данные для формы заказа
            'last_name': request.user.last_name,
        }

        form = CreateOrderForm(initial=initial)

    return render(request, 'orders/create_order.html', {'form': form, 'orders': True})

