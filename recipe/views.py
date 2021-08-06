from django.shortcuts import render
import json

# Create your views here.
def search_recipes(request):
    return render(request,'recipe/search_recipes.html')
def create_recipe(request,id=-1):
    return render(request,'recipe/create_recipe.html')
def recipe(request,id):
    return render(request,'recipe/recipe.html',context={'id':id})
def meal(request,ids):
    ids = json.loads(ids)
    return render(request,'recipe/meal.html',context={'ids':ids})
def help(request):
    return render(request,'recipe/help.html')