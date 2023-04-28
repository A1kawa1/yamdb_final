from api.v1.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                          ReviewViewSet, TitleViewSet, UserViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.v1.views import register, get_jwt_token


router = DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register(r"users", UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', register, name='register'),
    path('auth/token/', get_jwt_token, name='token')
]
