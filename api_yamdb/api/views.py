from rest_framework import filters, mixins, viewsets
from reviews.models import Category, Genre, Title

from .permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          GetTitleSerializer, PostTitleSerializer)


class CreateDeleteViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class CategoryViewSet(CreateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class GenreViewSet(CreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return PostTitleSerializer
        return GetTitleSerializer
