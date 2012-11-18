from django.contrib import admin
from recipe.models import Recipe, Amount, Step, RecipeCategory, Vote, DidRecipe
import autocomplete_light

class AmountInline(admin.TabularInline):
	model = Amount
	extra = 5

class StepInline(admin.TabularInline):
	model = Step
	extra = 10

class VoteInline(admin.TabularInline):
	model = Vote

class RecipeInline(admin.TabularInline):
	model = Recipe

class RecipeAdmin(admin.ModelAdmin):
	inlines = (AmountInline, StepInline, VoteInline, )
	form = autocomplete_light.modelform_factory(Recipe)

class RecipeCategoryAdmin(admin.ModelAdmin):
	inlines = (RecipeInline, )

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Amount)
admin.site.register(Step)
admin.site.register(Vote)
admin.site.register(DidRecipe)
admin.site.register(RecipeCategory, RecipeCategoryAdmin)
