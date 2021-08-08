from django import template

register = template.Library()

@register.filter(name="get_right_ingredients")
def get_right_ingredients(obj, multiplier):
    return obj.ingredientsAsText(multiplier)