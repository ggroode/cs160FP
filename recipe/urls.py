from django.urls import include, path
from . import views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("",views.search_recipes,name='index'),
    path("search-recipes",views.search_recipes,name='search-recipes'),
]