from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display =  [
        'id',
        'name_ru',
        'name_uz'
    ]
    class Meta:
        model = Category

admin.site.register(Category, CategoryAdmin)