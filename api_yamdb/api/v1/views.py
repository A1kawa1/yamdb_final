from http import HTTPStatus
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, User, Title
from api_yamdb.settings import ADMIN_EMAIL
from api.v1.filters import TitleFilter
from api.v1.permissions import (IsAdminOrReadOnly, IsAuthOrStaffOrReadOnly,
                                OwnerOrAdmins)
from api.v1.serializers import (CategorySerializer, CommentSerializer,
                                GenreSerializer, MeSerializer,
                                RegisterDataSerializer, ReviewSerializer,
                                TitleSerializerCreate, TitleSerializerRead,
                                TokenSerializer, UserSerializer)


class GetPostDestroy(
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Класс родитель для получения, записи, удаления"""
    pass


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведений"""

    queryset = Title.objects.all()
    serializer_class = TitleSerializerRead
    filter_backends = (DjangoFilterBackend,)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleSerializerCreate
        return TitleSerializerRead


class GenreViewSet(GetPostDestroy):
    """Вьюсет для жанров"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    )
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(GetPostDestroy):
    """Вьюсет для катекорий"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    )
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов"""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthOrStaffOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(
            author=self.request.user,
            title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев"""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthOrStaffOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(
            Review,
            id=review_id,
            title=title_id
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(
            Review,
            id=review_id
        )
        serializer.save(
            author=self.request.user,
            review=review
        )


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для пользователей"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (OwnerOrAdmins,)
    filter_backends = (SearchFilter,)
    filterset_fields = ("username",)
    search_fields = ("username",)
    lookup_field = "username"
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(methods=["GET", "PATCH"],
            detail=False,
            url_path="me",
            permission_classes=(IsAuthenticated,))
    def users_own_profile(self, request):
        user = request.user
        if request.method == "GET":
            serializer = MeSerializer(user)
            return Response(serializer.data, status=HTTPStatus.OK)
        serializer = MeSerializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTPStatus.OK)


@api_view(["POST"])
def get_jwt_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )
    token = AccessToken.for_user(user)
    return Response({"token": str(token)}, status=HTTPStatus.OK)


@api_view(["POST"])
def register(request):
    serializer = RegisterDataSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        user = User(
            username=username,
            email=email
        )
        user.save()
    else:
        email = serializer.data.get('email')
        username = serializer.data.get('username')
        try:
            user = User.objects.get(
                username=username,
                email=email
            )
        except User.DoesNotExist:
            serializer.is_valid(raise_exception=True)

    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject="YaMDb registration",
        message=f"Your confirmation code: {confirmation_code}",
        from_email=ADMIN_EMAIL,
        recipient_list=[user.email],
    )
    return Response(serializer.data, status=HTTPStatus.OK)
