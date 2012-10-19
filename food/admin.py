from django.contrib import admin
from food.models import Food
from food.models import FoodCategory
from recipe.admin import AmountInline

class FoodAdmin(admin.ModelAdmin):
	inlines = (AmountInline, )

admin.site.register(Food, FoodAdmin)
admin.site.register(FoodCategory)
