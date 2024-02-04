from django.contrib import admin
from api.models import Product


@admin.register(Product)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'price']
