from django.shortcuts import render, redirect
import json
from .models import Recipe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
# Create your views here.
def search_recipes(request):
    name = request.GET.get("name","")
    recipes = Recipe.objects.filter(name__contains=name)
    return render(request,'recipe/search_recipes.html',context={'recipes':recipes})

@csrf_exempt
def create_recipe(request,rid=-1):
    if not request.user.is_authenticated:
        return redirect('accounts/login')
    if request.method == "POST":
        # add recipe to database
        id = 4
        recipe = Recipe.objects.get(id=id)
        test = 0
        return redirect('recipe/{}'.format(id), context={'id':id,'recipe':recipe,'test':test})
    context={'classifications':Recipe.Classifications}
    if rid != -1:
        r = Recipe.objects.get(id=rid)
        if r.author.id != request.user.id:
            pass;
        else:
            pass;
    return render(request,'recipe/create_recipe.html', context)

def edit_recipe(request, rid):
    if not request.user.is_authenticated:
        return redirect('accounts/login')
    return render(request,'recipe/create_recipe.html',context={'classifications':Recipe.Classifications})

def recipe(request,id):
    test = request.GET.get("test",1)
    recipe = Recipe.objects.get(id=id)
    return render(request,'recipe/recipe.html',context={'id':id,'recipe':recipe,'test':test})
def meal(request,ids):
    ids = ids.split(",")
    recipes = Recipe.objects.filter(id__in=ids)
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
