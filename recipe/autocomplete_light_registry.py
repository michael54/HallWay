import autocomplete_light

from recipe.models import Recipe

autocomplete_light.register(Recipe, search_fields=('name',), autocomplete_js_attributes={'placeholder': 'recipe name ..'})