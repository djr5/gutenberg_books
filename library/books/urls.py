from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BooksDetailsListViewset

default_router = DefaultRouter(trailing_slash=False)
default_router.register("", BooksDetailsListViewset, basename='books')

urlpatterns = [
    path('', include(default_router.urls)),
]