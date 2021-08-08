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
    path("meal/<str:ids>/shopping-list",views.shoppingList,name='shopping-list'),
    #path("meal",views.meal,name='meal'),
    path("help",views.help,name='help'),
    path("get_new_ing_list", views.get_new_ing_list,name="get_new_ing_list"),
    path("rate", views.rate,name="rate"),
    path("register", views.register, name="register"),
]
