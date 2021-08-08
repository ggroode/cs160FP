from django.shortcuts import render
import json
from .models import Recipe
# Create your views here.
def search_recipes(request):
    recipes = Recipe.objects.all()
    return render(request,'recipe/search_recipes.html',context={'recipes':recipes})
def create_recipe(request,id=-1):
    return render(request,'recipe/create_recipe.html',context={'classifications':Recipe.Classifications})
def recipe(request,id):
    recipe = Recipe.objects.filter(id=id)[0]
    return render(request,'recipe/recipe.html',context={'id':id,'recipe':recipe })
def meal(request,ids):
    recipes = Recipe.objects.all()
    ids = json.loads(ids)
    return render(request,'recipe/meal.html',context={'ids':ids, 'recipes' :recipes})
def help(request):
    return render(request,'recipe/help.html')
def shoppingList(request,ids):
    return render(request,'recipe/base.html')

