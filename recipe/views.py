from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
import json
from .models import Recipe,User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db.models import Q, Avg, Count,Max
import re

# Create your views here.
def search_recipes(request):
    #getting search parameters
    name = request.GET.get("name","")
    authors = request.GET.get('author',"")
    tags = request.GET.get('tags',"")
    ingredients = request.GET.get('ingredients',"")
    private = bool(request.GET.get('visibility-private',False))
    public =bool(request.GET.get('visibility-public',False))
    entree = bool(request.GET.get('classification-entree',False))
    side = bool(request.GET.get('classification-side',False))
    appetizer = bool(request.GET.get('classification-appetizer',False))
    dessert = bool(request.GET.get('classification-dessert',False))
    drink = bool(request.GET.get('classification-drink',False))
    minRating = float(request.GET.get('rating-min',0))
    maxRating = float(request.GET.get('rating-max',5))
    minCookingTime = float(request.GET.get('cooking time-min',0))
    maxCookingTime = float(request.GET.get('cooking time-max',"")) if request.GET.get('cooking time-max',"") else Max('cookingTime')

    if not (private or public):
        private = True
        public = True
    if not (entree or side or appetizer or dessert or drink):
        entree=True
        side = True
        appetizer = True
        dessert = True
        drink = True
    # putting search parameters in proper form and filtering
    if request.user.is_authenticated:
        recipes = Recipe.objects.filter(Q(private=False) | Q(private=True,author=request.user))
    else:
        recipes=Recipe.objects.filter(private=False)
    recipes = recipes.filter(name__contains=name)
    if authors:
        authors = re.split("[^\w]+",authors)
        authorList = User.objects.filter(username__in=authors)
        recipes = recipes.filter(author__in= authorList)
    if tags:
        tags = re.split("[^\w]+",tags)
        for tag in tags:
            recipes = recipes.filter(tag__name=tag)
    if ingredients:
        ingredients=[s.lower() for s in re.split("[^\w]+",ingredients)]
        for ing in ingredients:
            recipes = recipes.filter(ingredient__name=ing)
    if not (private and public):
        recipes = recipes.filter(private=private)
    if (entree or side or appetizer or dessert or drink) and not (entree and side and appetizer and dessert and drink):
        classifications = []
        if entree:
            classifications.append('en')
        if side:
            classifications.append('si')
        if appetizer:
            classifications.append('ap')
        if dessert:
            classifications.append('de')
        if drink:
            classifications.append('dr')
        recipes = recipes.filter(classification__in=classifications)
    recipes = recipes.annotate(avg_rating=Avg('rating__value'))
    if minRating ==0:
        recipes = recipes.annotate(rating_count=Count('rating'))
        recipes = recipes.filter(Q(avg_rating__lte=maxRating)|Q(rating_count=0))
    else:
        recipes = recipes.filter(avg_rating__gte=minRating,avg_rating__lte=maxRating)
    recipes = recipes.filter(cookingTime__lte=maxCookingTime,cookingTime__gte=minCookingTime)
    if not request.GET.get('cooking time-max',""):
        maxCookingTime='∞'
    print(authors,tags)
    #Setting backup filters
    filters = zip(
    ['visibility','classification','rating','cooking time','author','tags','ingredients'],
    ['multi-select','multi-select','numeric','numeric','text','text','text'],
    [zip(('public','private'),(public,private)),zip(('entree','side','dessert','appetizer','drink'),(entree,side,dessert,appetizer,drink)),
        (0,5,'stars',minRating,maxRating),(0,'∞','min',minCookingTime,maxCookingTime),[",".join(authors)],[",".join(tags)],[",".join(ingredients)]]
    )
    return render(request,'recipe/search_recipes.html',context={'recipes':recipes,'filters':filters})

@csrf_exempt
def create_recipe(request,rid=-1):
    if not request.user.is_authenticated:
        return redirect('accounts/login')
    if request.method == "POST":
        # add recipe to database
        # print("\n\n")
        # for k, v in request.POST.items():
        #     print(k, v)
        # print("\n\n")
        # Recipe.createRecipe()
        d1 = request.POST
        d2 = {}
        for k, v in request.POST.items():
            d2[k] = v
        d2["private"] = True if d2["private"] == "true" else False
        d2["tags"] = d2["tags"].split(",")
        d2["steps"] = d2["steps"].split(",")
        d2["image"] = request.FILES['files[]']
        # print("\n\n")
        # print(d2["steps"])
        # print(d2["tags"])
        # print(d2["ingredients"])
        d2["ingredients"] = json.loads(d2["ingredients"])
        # print(d2["ingredients"])
        # print("\n\n")
        if rid != -1:
            Recipe.objects.get(id=rid).delete()
            d2["id"] = rid
            # recipe.setid(rid)
        recipe = Recipe.createRecipeFromDict(d2)
        id = recipe.id
        test = 0
        return redirect('/recipe/{}'.format(id), context={'id':id,'recipe':recipe,'test':test})
    context={'classifications':Recipe.Classifications}
    if rid != -1:
        r = Recipe.objects.get(id=rid)
        if r.author.id != request.user.id:
            return redirect('/recipe/{}?flash=You%20may%20only%20edit%20your%20own%20recipes%21'.format(rid), context={'id':rid,'recipe':r,'test':0})
        else:
            context["recipe"] = r
            context["tags"] = r.tags
            context["ingredients"] = [[i, r.ingredients[i]["quantity"], r.ingredients[i]["unit"]] for i in r.ingredients.keys()]
            # return render(request,'recipe/create_recipe.html', context)
    return render(request,'recipe/create_recipe.html', context)

# def edit_recipe(request, rid):
#     if not request.user.is_authenticated:
#         return redirect('accounts/login')
#     return render(request,'recipe/create_recipe.html',context={'classifications':Recipe.Classifications})

def recipe(request,id):
    test = request.GET.get("test",1)
    recipe = Recipe.objects.get(id=id)
    return render(request,'recipe/recipe.html',context={'id':id,'recipe':recipe,'test':test,'classifications':Recipe.Classifications})
def meal(request,ids):
    page = int(request.GET.get('page',1))
    recPerPage = int(request.GET.get('recPerPage',3))
    idsList = ids.split(",")
    recipes = list(Recipe.objects.filter(id__in=idsList))[(page-1)*recPerPage:page*recPerPage]
    return render(request,'recipe/meal.html',context={'ids':ids, 'recipes' :recipes})
def help(request):
    return render(request,'recipe/help.html')
def shoppingList(request,ids):
    #get list of recipes from ids.
    idsList = ids.split(",")
    recipes = Recipe.objects.filter(id__in=idsList)
    #get merged ingredients from Recipe.mergeIngredients
    mergedIngredients = Recipe.mergeIngredients(recipes)
    #convert to text with Recipe.ingredientsToText(ingredients)
    allIngredients = Recipe.ingredientsToText(mergedIngredients, 1)
    #add that to the context and of course make it point to a correct html
    return render(request,'recipe/shoppingList.html', context={'ids': ids, 'allIngredients':allIngredients})

@csrf_exempt
def get_new_ing_list(request):
    recipe_id = request.POST.get("id")
    multiplier = float(request.POST.get("mult"))
    recipe = Recipe.objects.filter(id=recipe_id)[0]
    newlist = recipe.ingredientsAsText(multiplier)
    return HttpResponse(','.join(newlist))

@csrf_exempt
def rate(request):
    rater = request.POST.get("rater")
    recipe_id = request.POST.get("id")
    rating = request.POST.get("rating")
    recipe = Recipe.objects.filter(id=recipe_id)[0]
    # recipe.ingredientsAsText(2)
    recipe.rate(rater,rating)
    return HttpResponse(1)
def register(request):
    if request.method == "GET":
        return render(
            request, "registration/register.html",
            {"form": UserCreationForm}
        )
    elif request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return search_recipes(request)
        return redirect(request.path+"?flash=Invalid Password!")

@csrf_exempt
def comment(request):
    rater = request.POST.get("rater")
    recipe_id = request.POST.get("id")
    content = request.POST.get("content")
    date_time = request.POST.get("date_time")
    recipe = Recipe.objects.filter(id=recipe_id)[0]
    recipe.comment(rater,content,date_time)
    return HttpResponse(1)
