from django.shortcuts import render
import json
from .models import Recipe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
# Create your views here.
def search_recipes(request):
    recipes = Recipe.objects.all()
    return render(request,'recipe/search_recipes.html',context={'recipes':recipes})
def create_recipe(request,id=-1):
    return render(request,'recipe/create_recipe.html',context={'classifications':Recipe.Classifications})
def recipe(request,id):
    test = request.GET.get("test",1) 
    recipe = Recipe.objects.filter(id=id)[0]
    return render(request,'recipe/recipe.html',context={'id':id,'recipe':recipe,'test':test})
def meal(request,ids):
    recipes = Recipe.objects.all()
    ids = json.loads(ids)
    return render(request,'recipe/meal.html',context={'ids':ids, 'recipes' :recipes})
def help(request):
    return render(request,'recipe/help.html')
def shoppingList(request,ids):
    return render(request,'recipe/base.html')

@csrf_exempt
def get_new_ing_list(request):
    recipe_id = request.POST.get("id")
    multiplier = float(request.POST.get("mult"))
    recipe = Recipe.objects.filter(id=recipe_id)[0]
    newlist = recipe.ingredientsAsText(multiplier)
    return HttpResponse(','.join(newlist))


