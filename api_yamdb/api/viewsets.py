from rest_framework import mixins, viewsets, filters
from rest_framework.pagination import PageNumberPagination

from .permissions import IsAdminOrReadOnly


class CreateDeleteListViewset(mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
