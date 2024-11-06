from django.contrib import admin
from api.models import Product, Album, Track


@admin.register(Product)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'price']


admin.site.register(Album)
admin.site.register(Track)
