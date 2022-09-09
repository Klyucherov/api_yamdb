from api.views import CategoryViewSet, GenreViewSet, TitleViewSet
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
