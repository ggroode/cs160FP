from django import template
from ..models import Rating

register = template.Library()

@register.filter(name="get_right_ingredients")
def get_right_ingredients(obj, multiplier):
    return obj.ingredientsAsText(multiplier)

@register.filter(name="get_rating")
def get_rating(user, id):
    if user.is_authenticated:
        r = Rating.objects.filter(author=user,recipe__id=id).first()
        if r:
            return r.value
    return 0