from django.contrib import admin
from reviews.models import (
    Title, Genre, Category,
    Review, Comment
)


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
        'category'
    )
    search_fields = (
        'name',
        'year',
        'category'
    )
    empty_value_display = 'пусто'


class GenreAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'slug'
    )
    search_fields = ('name',)
    empty_value_display = 'пусто'


class CategoryAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'slug'
    )
    search_fields = ('name',)
    empty_value_display = 'пусто'


class ReviewAdmin(admin.ModelAdmin):
    fields = (
        'title',
        'author',
        'pub_date',
        'text',
        'score'
    )
    search_fields = (
        'title',
        'author'
    )
    empty_value_display = 'пусто'


class CommentAdmin(admin.ModelAdmin):
    fields = (
        'review',
        'author',
        'pub_date',
        'text'
    )
    search_fields = (
        'review',
        'author'
    )
    empty_value_display = 'пусто'


admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
