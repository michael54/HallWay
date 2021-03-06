from django.contrib import admin
from recipe.models import Recipe, Amount, Step, RecipeCategory, Vote, DidRecipe

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

class RecipeCategoryAdmin(admin.ModelAdmin):
	inlines = (RecipeInline, )

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Amount)
admin.site.register(Step)
admin.site.register(Vote)
admin.site.register(DidRecipe)
admin.site.register(RecipeCategory)
