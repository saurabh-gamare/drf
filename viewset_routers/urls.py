# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register('books', BookViewSet, basename='books')

# basename is an optional arg, by default it will use model name.
# for different methods, it will use <basename> + '-list', '-create', '-update', etc
# eg: books-list

urlpatterns = [
    path('', include(router.urls)),
]
