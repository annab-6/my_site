from django.shortcuts import render


def index(request):
    """
        Обработки запроса на главную страницу.

       arguments:
       - request: HttpRequest объект, представляющий текущий HTTP запрос.

       return:
       - HttpResponse объект, содержащий HTML-страницу для главной страницы.

       context:
       - title: Заголовок страницы.
       - content: Контент страницы.

       usage
       - Переход на главную страницу в браузере.
       """

    context = {
        "title": "Main | House of Fragrance",
        "content": "HOUSE OF FRAGRANCE",

    }
    return render(request, "my_site/index.html", context)


def about(request):
    """
       Обработка запроса на страницу "About us".

       arguments:
       - request: HttpRequest объект, представляющий текущий HTTP запрос.

       returns:
       - HttpResponse объект, содержащий HTML-страницу для страницы "About us".

       context:
       - title: Заголовок страницы.
       - content: Контент страницы "About us".

       usage:
       - Переход на страницу "About us" в браузере.
       """
    context = {
        "title": "About us | House of Fragrance ",
        "content": "Ａｂｏｕｔ Ｕｓ",

    }
    return render(request, "my_site/about.html", context)
