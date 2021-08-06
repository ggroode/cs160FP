from django.shortcuts import render

# Create your views here.
def search_recipes(request):
    return render(request,'recipe/search_recipes.html')
