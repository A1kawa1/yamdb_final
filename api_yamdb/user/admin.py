from django.contrib import admin
from user.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'role',
        'bio'
    )
    search_fields = ('username', 'first_name')
    empty_value_display = 'пусто'


admin.site.register(User, UserAdmin)
