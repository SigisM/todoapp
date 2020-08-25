import django_filters
from .models import Todo

import django_filters

class PostFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Todo
        fields = ['title',]