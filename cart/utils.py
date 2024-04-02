from cart.models import Cart


def get_user_cart(request):
    """
       Функция для получения корзины пользователя.

       Если пользователь аутентифицирован, функция возвращает корзину пользователя, связанную с его аккаунтом.
       Если пользователь не аутентифицирован, функция создает сеанс веб-сессии и возвращает корзину,
       связанную с этим сеансом.

       Возвращаемая корзина содержит объекты Cart, связанные с продуктами (через select_related).
       """
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).select_related('product')

    if not request.session.session_key:
        request.session.create()
    return Cart.objects.filter(session_key=request.session.session_key).select_related('product')
