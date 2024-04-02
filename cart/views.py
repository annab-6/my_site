from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from cart.models import Cart
from cart.utils import get_user_cart
from products.models import Products


def add_cart(request):
    try:
        product_id = request.POST.get("product_id")     # Получает ID товара из параметров запроса.
        product = Products.objects.get(id=product_id)   # Ищет товар в базе данных по его ID.
        user = request.user
        if user.is_authenticated:
            # создает новую запись в корзине для этого пользователя с данным товаром
            cart, created = Cart.objects.get_or_create(user=user, product=product)
        else:
            # или увеличивает количество, если запись уже существует.
            session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key, product=product)
        if not created:
            #Если не аутентифицирован, создает новую запись в корзине сессии с данным товаром или увеличивает количество,
            cart.quantity += 1
            cart.save()
    except ObjectDoesNotExist:
        return JsonResponse({"message": "Product not found"}, status=404)

    user_cart = get_user_cart(request)
    cart_items_html = render_to_string("cart/includes/included_cart.html", {"carts": user_cart}, request=request)
    response_data = {
        "message": "Product added to cart",
        "cart_items_html": cart_items_html,
    }
    return JsonResponse(response_data)


def change_cart(request):
    try:
        cart_id = request.POST.get("cart_id")
        quantity = request.POST.get("quantity")
        cart = Cart.objects.get(id=cart_id)
        cart.quantity = quantity
        cart.save()
        updated_quantity = cart.quantity
    except ObjectDoesNotExist:
        return JsonResponse({"message": "Cart item not found"}, status=404)

    user_cart = get_user_cart(request)
    cart_items_html = render_to_string("cart/includes/included_cart.html", {"carts": user_cart}, request=request)
    response_data = {
        "message": "Quantity changed",
        "cart_items_html": cart_items_html,
        "quantity": updated_quantity,
    }
    return JsonResponse(response_data)


def delete_cart(request):
    try:
        cart_id = request.POST.get("cart_id")
        cart = Cart.objects.get(id=cart_id)
        quantity = cart.quantity
        cart.delete()
    except ObjectDoesNotExist:
        return JsonResponse({"message": "Cart item not found"}, status=404)

    user_cart = get_user_cart(request)
    cart_items_html = render_to_string("cart/includes/included_cart.html", {"carts": user_cart}, request=request)
    response_data = {
        "message": "Product removed",
        "cart_items_html": cart_items_html,
        "quantity_deleted": quantity,
    }
    return JsonResponse(response_data)
