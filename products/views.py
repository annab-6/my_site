from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from products.models import Products
from products.utils import search_products

from products.models import Categories


def display_products(request, category_slug=None):
    """
        Функция для отображения списка продуктов на странице.

        args:
        - request: объект HttpRequest, представляющий текущий HTTP-запрос.
        - category_slug: строка, содержащая слаг категории продуктов (по умолчанию None).

        returns:
        - HttpResponse: объект, содержащий HTML-страницу со списком продуктов.

        context:
        - title: заголовок страницы.
        - products: список продуктов, отображаемых на текущей странице.
        - slug_url: слаг категории, используемый в URL (если задан).

        usage:
        - Посещение страницы со списком продуктов в веб-браузере.
        """

    page = request.GET.get("page", 1) # извлекает значение параметра page из GET-запроса. Если параметр page отсутствует в запросе, оно по умолчанию устанавливается равным 1.
    order_by = request.GET.get("order_by", None) #извлекает значение параметра order_by из GET-запроса. Если параметр order_by отсутствует в запросе, устанавливается значение None
    query = request.GET.get("q", None) # извлекает значение параметра q из GET-запроса. Если параметр q отсутствует в запросе, устанавливается значение None.

    if category_slug == "all":# проверяет, равен ли category_slug "all" или пуст ли он (не предоставлен). Если хотя бы одно из условий истинно, извлекаются все продукты.
        products = Products.objects.all()
    elif query:                           #  Этот блок проверяет, есть ли поисковый запрос (query не равно None). Если да, вызывается функция search_products для извлечения соответствующих продуктов.
        products = search_products(query)
    else:                 #Если ни одно из вышеперечисленных условий не выполняется, предполагается, что предоставлена конкретная категория ( category_slug не равно "all" и не пустая), и извлекаются продукты, принадлежащие этой категории.
        category = get_object_or_404(Categories, slug=category_slug)
        products = Products.objects.filter(category=category)

    if order_by:
        products = products.order_by(order_by)  #Этот блок условия проверяет, предоставлен ли параметр order_by в запросе. Если да, соответствующим образом применяется сортировка к продуктам.

    paginator = Paginator(products, 3) #Эта строка создает объект paginator для разбиения извлеченных продуктов на страницы. Указывается, что на каждой странице должно быть 3 продукта.
    current_page = paginator.page(page)  #Эта строка извлекает запрошенную страницу продуктов из пагинатора на основе параметра page, извлеченного из GET-запроса.

    context = {                          #содержит данные, которые будут переданы в шаблон. В него включается заголовок страницы, продукты для отображения на текущей странице и category_slug для навигации по URL.
        "title": "Products | House of Fragrance",
        "products": current_page,
        "slug_url": category_slug
    }

    return render(request, "products/products.html", context) #отображает шаблон products.html с предоставленными данными контекста и возвращает его в виде HTTP-ответа.


def display_item(request, item_slug):
    """
        Функция для отображения отдельного продукта.

        Args:
        - request: объект HttpRequest, представляющий текущий HTTP-запрос.
        - item_slug: строка, содержащая слаг продукта.

        Returns:
        - HttpResponse: объект, содержащий HTML-страницу с отдельным продуктом.

        Context:
        - item: объект продукта, который будет отображен на странице.

        Example usage:
        - Посещение страницы с отдельным продуктом в веб-браузере.
        """

    item = get_object_or_404(Products, slug=item_slug)

    context = {
        "item": item
    }
    return render(request, "products/item.html", context=context)
