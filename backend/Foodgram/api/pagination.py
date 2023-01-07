"""Описания классов пагинации."""

from rest_framework.pagination import PageNumberPagination


class LimitPageNumberPagination(PageNumberPagination):
    """Переопределение класса PageNumberPagination:
    вывод лимитированного количества рецептов по запросу параметра limit."""
    page_size_query_param = 'limit'
