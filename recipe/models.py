from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.core.validators import MaxValueValidator
from nltk.stem import PorterStemmer
import re
  
ps = PorterStemmer()

def pluralize(noun):
    if re.search('[sxz]$', noun):
         return re.sub('$', 'es', noun)
    elif re.search('[^aeioudgkprt]h$', noun):
        return re.sub('$', 'es', noun)
    elif re.search('[aeiou]y$', noun):
        return re.sub('y$', 'ies', noun)
    else:
        return noun + 's'

# Create your models here.
def get_list():
    return []

class Recipe(models.Model):
    class Classifications(models.TextChoices):
        DESSERT = 'de'
        ENTREE = 'en'
        SIDE = 'si'
        APPETIZER = 'ap'
        DRINK ='dr' 
 
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    cookingTime = models.IntegerField()
    image = models.ImageField()
    classification = models.CharField(max_length=2,choices=Classifications.choices,default=Classifications.ENTREE)
    servings = models.IntegerField()
    servingSize = models.CharField(max_length=50)
    author = models.ForeignKey(User,on_delete=CASCADE)
    private = models.BooleanField(default=False)
    ingredients = models.JSONField(default=dict)
    steps = models.JSONField(default=get_list)
    @property
    def tags(self):
        return [tag.name for tag in Tag.objects.filter(recipe_id=self.id)]
    @property
    def comments(self):
        return Comment.objects.filter(recipe_id=self.id)
    @property
    def rating(self):
        ratings = Rating.objects.filter(recipe_id=self.id)
        if len(ratings)==0:
            return 0
        return sum(ratings)/len(ratings)

    def rate(self,userName,ratingValue):
        # assert ratingValue in [1,2,3,4,5]
        user = User.objects.get(username=userName)
        rating = Rating.objects.filter(recipe_id=self.id,author=user).first()
        if rating:
            rating.value = ratingValue
        else:
            Rating.objects.create(recipe=self,author=user,value=ratingValue)
            

    def addIngredient(self,ingredientName,unit,quantity):
        ingredientName = " ".join([ps.plur2sing(word) for word in ingredientName.split(' ')])
        self.ingredients[ingredientName] = {'quantity':quantity, 'unit':unit}
        ing = Ingredient.objects.filter(name=ingredientName).first()
        if not ing:
            ing = Ingredient.objects.create(name=ingredientName)
        ing.recipes.add(self)

    def addStep(self,stepText):
        self.steps.append(stepText)
    
    def ingredientsAsText(self,multiplier=1):
        return Recipe.ingredientsToText(self.ingredients,multiplier=1)

    def addTag(self,tagName):
        tag = Tag.objects.filter(name=tagName).first()
        if not tag:
            tag = Tag.objects.create(name=tagName)
        tag.recipes.add(self)
    
    @staticmethod
    def mergeIngredients(recipeList):
        ingredients = dict()
        for recipe in recipeList:
            for ingredientName in recipe.ingredients.keys():
                if ingredientName in ingredients:
                    if ingredients[ingredientName]['unit'] == recipe.ingredients[ingredientName]['unit']:
                        ingredients[ingredientName]['quantity'] += recipe.ingredients[ingredientName]['quantity']
                    else:
                        pass
                else:
                    ingredients[ingredientName] = recipe.ingredients[ingredientName]
        return ingredients
    
    @staticmethod
    def createRecipe(name,description,cookingTime,image,classification,servings,servingSize,authorUserName,private=False,ingredients=[],steps=[],tags=[]):
        user = User.objects.get(username=authorUserName)
        r = Recipe(name=name,description=description,cookingTime=cookingTime,image=image,classification=classification,servings=servings,servingSize=servingSize,author=user,private=private)
        r.save()
        for name,quantity,unit in ingredients:
            r.addIngredient(name,unit,quantity)
        for step in steps:
            r.addStep(step)
        for tag in tags:
            r.addTag(tag)
    
    @staticmethod
    def ingredientsToText(ingredients,multiplier=1):
        ingTextList=[]
        for name in ingredients.keys():
            ing = ingredients[name]
            unit,quantity = ing['unit'],ing['quantity']*multiplier
            if unit in ['count','cnt']:
                if quantity == 1:
                    ingTextList.append("{} {}".format(quantity,name))
                else:
                    ingTextList.append("{} {}".format(quantity,pluralize(name)))
            else:
                ingTextList.append("{} {} of {}".format(quantity,unit,pluralize(name)))
        return ingTextList

class Meal(models.Model):
    name = models.CharField(max_length=50)
    recipes = models.ManyToManyField(Recipe)
    author = models.ForeignKey(User,on_delete=CASCADE)

class Tag(models.Model):
    name = models.CharField(max_length=15, unique=True,primary_key=True)
    recipes = models.ManyToManyField(Recipe)

class Ingredient(models.Model):
    name = models.CharField(max_length=15, unique=True,primary_key=True)
    recipes= models.ManyToManyField(Recipe)

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe,on_delete=CASCADE)
    author = models.ForeignKey(User,on_delete=CASCADE)
    content = models.CharField(max_length=500)
    date_modified = models.DateTimeField(auto_now=True)

class Rating(models.Model):
    recipe = models.ForeignKey(Recipe,on_delete=CASCADE)
    author = models.ForeignKey(User,on_delete=CASCADE)
    value = models.IntegerField(validators=[MaxValueValidator(5)]) #1,2,3,4,5

