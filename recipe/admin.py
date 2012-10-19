from django.contrib import admin
from recipe.models import Recipe, Amount

class AmountInline(admin.TabularInline):
	model = Amount

class RecipeAdmin(admin.ModelAdmin):
	inlines = (AmountInline,)


admin.site.register(Recipe, RecipeAdmin)
