from django.db.models import Avg
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from http import HTTPStatus
from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import year_validate
from user.validators import validate_username


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'name',
            'slug'
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'name',
            'slug'
        )


class TitleSerializerRead(serializers.ModelSerializer):
    category = CategorySerializer(
        many=False,
        required=True
    )
    genre = GenreSerializer(
        many=True,
        required=False
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        read_only_fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score'))['score__avg']
        return rating


class TitleSerializerCreate(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        many=False
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        required=False,
    )
    year = serializers.IntegerField(
        validators=[
            year_validate
        ]
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )
    score = serializers.IntegerField(
        validators=[
            MinValueValidator(0, 'оценка должна быть больше 0'),
            MaxValueValidator(10, 'оценка должна быть меньше 10')
        ]
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'title',
            'author',
            'score',
            'pub_date'
        )
        read_only_fields = ('title',)

    def validate(self, data):
        request = self.context.get('request')
        author = request.user
        if request.method == 'POST':
            title_id = self.context.get('view').kwargs.get('title_id')
            title = get_object_or_404(Title, pk=title_id)
            if Review.objects.filter(
                    author=author,
                    title=title
            ).exists():
                raise serializers.ValidationError(
                    'нельзя оставить отзыв дважды'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User


class MeSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        user = get_object_or_404(
            User,
            username=username
        )

        if not default_token_generator.check_token(
            user, confirmation_code
        ):
            raise serializers.ValidationError(
                {
                    'confirmation_code': 'неверный код подтверждения'
                },
                HTTPStatus.BAD_REQUEST
            )
        return data


class RegisterDataSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            validate_username,
            UniqueValidator(queryset=User.objects.all())
        ],
        max_length=150,
        required=True
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        fields = (
            "username",
            "email"
        )
        model = User
