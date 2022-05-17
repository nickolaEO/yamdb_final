from django.contrib import admin

from api_yamdb.settings import EMPTY_VALUE_DISPLAY

from . import models


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'confirmation_code', 'role')
    search_fields = ('username', 'email',)
    list_filter = ('role',)
    empty_value_display = EMPTY_VALUE_DISPLAY


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug'
    )
    list_editable = ('name', 'slug')
    search_fields = ('id', 'name', 'slug',)
    list_filter = ('name', 'slug',)
    empty_value_display = EMPTY_VALUE_DISPLAY


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug'
    )
    list_editable = ('name', 'slug')
    search_fields = ('id', 'name', 'slug',)
    list_filter = ('name', 'slug',)
    empty_value_display = EMPTY_VALUE_DISPLAY


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'year',
        'category'
    )
    list_editable = ('name', 'year', 'category')
    search_fields = ('id', 'name', 'year',)
    list_filter = ('name', 'year',)
    empty_value_display = EMPTY_VALUE_DISPLAY


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'text',
        'pub_date',
        'author',
        'score',
    )
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = EMPTY_VALUE_DISPLAY


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'review',
        'author',
        'text',
        'pub_date',
    )
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = EMPTY_VALUE_DISPLAY


admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Genre, GenreAdmin)
admin.site.register(models.Title, TitleAdmin)
admin.site.register(models.Review, ReviewAdmin)
admin.site.register(models.Comment, CommentAdmin)
