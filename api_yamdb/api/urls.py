from django.urls import include, path
from rest_framework import routers

from .views import CommentViewSet, ReviewViewSet


app_name = 'api'
router_v1 = routers.DefaultRouter()
router_v1.register(
    r'titles/(?P<title_id>[^/.]+)/reviews',
    ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments',
    CommentViewSet,
    basename='comments'
)
urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
