from django.utils.http import urlencode


from django import template

from products.models import Categories

register = template.Library()


@register.simple_tag()
def tag_categories():
    """
      Функция для получения списка категорий и их отображения в шаблоне.

      Returns:
      - QuerySet: список объектов Categories.
      """
    return Categories.objects.all


@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    """
      Функция для изменения параметров URL на основе текущего контекста шаблона.

      Args:
      - context: контекст шаблона, содержащий объект запроса.
      - kwargs: произвольное количество именованных аргументов для изменения параметров URL.

      Returns:
    - str: строка с измененными параметрами URL.
    """
    # Извлечение словаря параметров GET из контекста шаблона
    query = context['request'].GET.dict()
    # Обновление параметров URL с помощью переданных аргументов kwargs
    query.update(kwargs)
    # Преобразование обновленного словаря параметров в строку параметров URL с помощью urlencode
    return urlencode(query)
