from django.contrib import admin
from .models import Recipe, Ingredient,Tag,Meal

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(Meal)
# Register your models here.
