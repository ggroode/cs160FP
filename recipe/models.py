from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.core.validators import MaxValueValidator
from nltk.stem import PorterStemmer
from pattern.en import pluralize,singularize
import re

ps = PorterStemmer()

# def pluralize(noun):
#     if re.search('[sxz]$', noun):
#          return re.sub('$', 'es', noun)
#     elif re.search('[^aeioudgkprt]h$', noun):
#         return re.sub('$', 'es', noun)
#     elif re.search('[aeiou]y$', noun):
#         return re.sub('y$', 'ies', noun)
#     else:
#         return noun + 's'

# Create your models here.
def get_list():
    return []

class Recipe(models.Model):
    COUNTNAMES=['cnt','count','Count','']
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
    def classificationName(self):
        return dict(Recipe.Classifications.choices)[self.classification]
    @property
    def tags(self):
        return [tag.name for tag in Tag.objects.filter(recipes__id=self.id)]
    @property
    def comments(self):
        return Comment.objects.filter(recipe_id=self.id)
    @property
    def rating(self):
        ratings = Rating.objects.filter(recipe_id=self.id)
        if len(ratings)==0:
            return 0
        totalvalue = 0
        for rate in ratings:
            totalvalue += rate.value
        return totalvalue/len(ratings)

    def setid(self, id):
        if id != -1:
            self.id = id
            self.save()

    def rate(self,userName,ratingValue):
        # assert ratingValue in [1,2,3,4,5]
        user = User.objects.get(id=userName)
        rating = Rating.objects.filter(recipe_id=self.id,author=user).first()

        if rating:
            rating.value = ratingValue
            rating.save()
        else:
            Rating.objects.create(recipe=self,author=user,value=ratingValue)

    def comment(self, userName,content,date_time):
        user = User.objects.get(id=userName)
        Comment.objects.create(recipe=self,author=user,content=content)


    def addIngredient(self,ingredientName,unit,quantity):
        # ingredientName = " ".join([singularize(word.lower()) for word in ingredientName.split(' ')])
        self.ingredients[ingredientName] = {'quantity':quantity, 'unit':unit}
        ing = Ingredient.objects.filter(name=ingredientName.lower()).first()
        if not ing:
            ing = Ingredient.objects.create(name=ingredientName.lower())
        ing.recipes.add(self)
        self.save()

    def addStep(self,stepText):
        self.steps.append(stepText)
        self.save()

    def ingredientsAsText(self,multiplier):
        return Recipe.ingredientsToText(self.ingredients,multiplier)

    @property
    def stepsAsHtml(self):
        steps = []
        for step in self.steps:
            steps.append("<h5>"+step+"</h5><br>")
        return steps

    def addTag(self,tagName):
        tag = Tag.objects.filter(name=tagName).first()
        if not tag:
            tag = Tag.objects.create(name=tagName)
        tag.recipes.add(self)

    @staticmethod
    def isCount(ingredient,unit):
        if unit in Recipe.COUNTNAMES:
            return True
        if singularize(unit.lower()) == singularize(ingredient.lower()):
            return True
        return False

    @staticmethod
    def pluralize(str):
        ending = str[-1]
        if ending in ['s','.']:
            return str
        return pluralize(str)

    @staticmethod
    def mergeIngredients(recipeList):
        ingredients = dict()
        ingredientsSing = dict()
        space = " "
        spaceCount=1
        for recipe in recipeList:
            for ingredientName in recipe.ingredients.keys():
                print(ingredientName)
                singName = singularize(ingredientName.lower())
                if singName in ingredientsSing.keys():
                    if singularize(ingredientsSing[singName]['unit'].lower()) == singularize(recipe.ingredients[ingredientName]['unit'].lower()) or (Recipe.isCount(ingredientName,ingredientsSing[singName]['unit']) and Recipe.isCount(ingredientName,recipe.ingredients[ingredientName]['unit'])):
                        
                        ingredients[ingredientName]['quantity'] = recipe.ingredients[ingredientName]['quantity'] + ingredientsSing[singName]['quantity']
                        # print(ingredients)[ingredientName]
                        ingredientsSing[singName]['quantity'] =  ingredients[ingredientName]['quantity']
                    else:
                        ingredients[ingredientName+space*spaceCount] = recipe.ingredients[ingredientName]
                        ingredients[singName+space*spaceCount]= recipe.ingredients[ingredientName]
                        spaceCount+=1
                else:
                    ingredients[ingredientName] = recipe.ingredients[ingredientName]
                    ingredientsSing[singName] = recipe.ingredients[ingredientName]
        return ingredients

    @staticmethod
    def createRecipe(name,description,cookingTime,image,classification,servings,servingSize,authorUserName,private=False,ingredients=[],steps=[],tags=[], optid = False):
        # user = User.objects.get(username=authorUserName)
        user = User.objects.get(id=authorUserName)
        r = Recipe(name=name,description=description,cookingTime=cookingTime,image=image,classification=classification,servings=servings,servingSize=servingSize,author=user,private=private)
        if optid:
            r.id = optid
        r.save()
        for name,quantity,unit in ingredients:
            r.addIngredient(name,unit,quantity)
        for step in steps:
            r.addStep(step)
        for tag in tags:
            r.addTag(tag)
        return r

    @staticmethod
    def createRecipeFromDict(dict):
        return Recipe.createRecipe(name = dict.get("name"), description = dict.get("description"),
         cookingTime = dict.get("cookingTime"), image = dict.get("image"),
         classification = dict.get("classification"), servings = dict.get("servings"),
         servingSize = dict.get("servingSize"), authorUserName = dict.get("author"),
         private = dict.get("private"), ingredients=dict.get("ingredients"),
         steps = dict.get("steps"), tags = dict.get("tags"), optid = dict.get("id"))

    @staticmethod
    def ingredientsToText(ingredients,multiplier):
        ingTextList=[]
        for name in ingredients.keys():
            ing = ingredients[name]
            unit,quantity = ing['unit'],ing['quantity']*multiplier
            if (quantity % 1 == 0):
                quantity = int(quantity)
                name = name.strip()
                if Recipe.isCount(name,unit):
                    if quantity == 1:
                        ingTextList.append("{} {}".format(quantity,name.capitalize()))
                    else:
                        ingTextList.append("{} {}".format(quantity,Recipe.pluralize(name).capitalize()))
                else:
                    if quantity==1:
                        ingTextList.append("{} {} of {}".format(quantity,unit,name.capitalize()))
                    else:
                        ingTextList.append("{} {} of {}".format(quantity,Recipe.pluralize(unit),name.capitalize()))
            else:
                if Recipe.isCount(name,unit):
                    ingTextList.append("{:.2f} {}".format(quantity,Recipe.pluralize(name).capitalize()))
                else:
                    ingTextList.append("{:.2f} {} of {}".format(quantity,Recipe.pluralize(unit),name.capitalize()))
        return ingTextList

    def __str__(self):
        return self.name

class Meal(models.Model):
    name = models.CharField(max_length=50)
    recipes = models.ManyToManyField(Recipe)
    author = models.ForeignKey(User,on_delete=CASCADE)

    @property
    def recipeNames(self):
        return [recipe.name for recipe in self.recipes.all()]

    @property
    def image(self):
        return self.recipes.first().image
    
    @property
    def ids(self):
        return ",".join([str(recipe.id) for recipe in self.recipes.all()])

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
