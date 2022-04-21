from django_filters import FilterSet, DateTimeFromToRangeFilter
from django_filters.widgets import RangeWidget
from .models import Post



# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.


class PostFilter(FilterSet):
    dateCreation = DateTimeFromToRangeFilter(lookup_expr=(
        'icontains'), widget=RangeWidget(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Post

        fields = {'author': ['exact'], 'title': ['icontains'],
                  #'postCategory': ['exact']
        }