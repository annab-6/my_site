from django import template

from cart.utils import get_user_cart

register = template.Library()


@register.simple_tag()
def user_cart(request):
    return get_user_cart(request)
