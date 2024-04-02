from django.contrib.postgres.search import SearchVector

from products.models import Products


def search_products(query):
    """
       Функция для поиска продуктов по заданному запросу.

       Args:
       - query: строка, содержащая поисковой запрос.

       Returns:
       - QuerySet: набор объектов Products, соответствующих запросу.

       Пример использования:
       - Вызов функции search_products для поиска продуктов, содержащих указанное слово в названии или описании.
       """

    # Проверяем, является ли запрос числом и имеет ли длину не более 5 символов
    if query.isdigit() and len(query) <= 5:
        # Если да, ищем продукты, содержащие это число в описании
        return Products.objects.filter(description__search=query)
    # В противном случае, используем поиск по вектору, включая поля "name" и "description"
    return Products.objects.annotate(search=SearchVector("name", "description")).filter(search=query)
