from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from nltk.stem import PorterStemmer

  
ps = PorterStemmer()

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

    def addIngredient(self,ingredientName,unit,quantity):
        self.save()
        ingredientName = " ".join([ps.stem(word) for word in ingredientName.split(' ')])
        self.ingredients[ingredientName] = {'quantity':quantity, 'unit':unit}
        if (Ingredient.objects.filter(name=ingredientName)):
            Ingredient.objects.get(name=ingredientName).recipes.add(self)
        else:
            ing = Ingredient.objects.create(name=ingredientName)
            ing.recipes.add(self)
            ing.save()
        self.save()
    def addStep(self,stepText):
        self.save()
        self.steps.append(stepText)
        self.save()
    def ingredientsAsText(self):
        return Recipe.ingredientsToText(self.ingredients)
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
        r = Recipe(name=name,description=description,cookingTime=cookingTime,image=image,classification=classification)
    @staticmethod
    def ingredientsToText(ingredients):
        for name in ingredients.keys():
            ing = ingredients[name]
               

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
    recipe_id = models.ForeignKey(Recipe,on_delete=CASCADE)
    author = models.ForeignKey(User,on_delete=CASCADE)
    value = models.IntegerField() #1,2,3,4,5

