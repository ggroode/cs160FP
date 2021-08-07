from django.urls import include, path
from . import views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("",views.search_recipes,name='index'),
    path("search-recipes",views.search_recipes,name='search-recipes'),
    path("create-recipe",views.create_recipe,name='create-recipe'),
    path("edit-recipe/<int:id>",views.create_recipe,name='edit-recipe'),
    path("recipe/<int:id>",views.recipe,name='recipe'),
    path("meal/<str:ids>",views.meal,name='meal'),
    path("meal",views.meal,name='meal'),
    path("help",views.help,name='help'),
]
