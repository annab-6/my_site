from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from cart.models import Cart
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm
from orders.models import Order, OrderItem
from django.db.models import Prefetch


def login(request):
    """
        Обрабатывает запросы на аутентификацию пользователя.

        Если метод запроса POST, пытается аутентифицировать пользователя.
        Если аутентификация успешна, пользователь входит в систему и перенаправляется на предыдущую страницу или домашнюю страницу.
        Если аутентификация не удалась или метод запроса не POST, отображается форма входа.

        :param request: объект HTTP-запроса
        :return: отображенная страница входа или перенаправление на предыдущую страницу или домашнюю страницу
        """
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)

            session_key = request.session.session_key

            if user:
                auth.login(request, user)
                messages.success(request, f"Welcome {username}! You have successfully logged in to your account")

                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

                next_url = request.POST.get('next')
                return HttpResponseRedirect(next_url or reverse('my_site:index'))

    else:
        form = UserLoginForm()

    context = {
        "title": "Authorization | House of Fragrance",
        "form": form
    }
    return render(request, "users/login.html", context)


def registration(request):
    """
       Обрабатывает запросы на регистрацию нового пользователя.

       Если метод запроса POST, пытается зарегистрировать нового пользователя.
       Если регистрация прошла успешно, пользователь входит в систему и перенаправляется на домашнюю страницу.
       Если регистрация не удалась или метод запроса не POST, отображается форма регистрации.

       :param request: объект HTTP-запроса
       :return: отображенная страница регистрации или перенаправление на домашнюю страницу
       """
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)

            session_key = request.session.session_key
            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

            messages.success(request, f"{user.username} You have successfully registered")
            return HttpResponseRedirect(reverse("my_site:index"))
    else:
        form = UserRegistrationForm()

    context = {
        "title": "Registration | House of Fragrance",
        "form": form

    }
    return render(request, "users/registration.html", context)


@login_required
def profile(request):
    """
       Отображает профиль пользователя и позволяет ему обновить свои данные.

       Если метод запроса POST, обновляет информацию профиля пользователя.
       Если обновление прошло успешно, отображается сообщение об успешном обновлении.
       Если метод запроса не POST, отображается форма профиля.

       :param request: объект HTTP-запроса
       :return: отображенная страница профиля
       """
    if request.method == "POST":
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "The page has been updated")
            return HttpResponseRedirect(reverse("users:profile"))
    else:
        form = ProfileForm(instance=request.user)

    orders = Order.objects.filter(user=request.user).prefetch_related(
                Prefetch(
                  "orderitem_set",
                  queryset=OrderItem.objects.select_related("product"),
                )
             ).order_by("-id")

    context = {
        "title": " Profile | House of Fragrance",
        'form': form,
        'orders': orders,

    }
    return render(request, "users/profile.html", context)


@login_required
def logout(request):
    """
       Выходит из текущего аккаунта пользователя и перенаправляет на домашнюю страницу.

       :param request: объект HTTP-запроса
       :return: перенаправление на домашнюю страницу
       """
    messages.success(request, "You are logged out!")
    auth.logout(request)
    return redirect(reverse("my_site:index"))
