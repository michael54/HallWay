from django.contrib import admin
from food.models import Food
from food.models import FoodCategory
from recipe.admin import AmountInline

class FoodInline(admin.TabularInline):
	model = Food

class FoodAdmin(admin.ModelAdmin):
	inlines = (AmountInline, )

class FoodCategoryAdmin(admin.ModelAdmin):
	inlines = (FoodInline, )

admin.site.register(Food, FoodAdmin)
admin.site.register(FoodCategory, FoodCategoryAdmin)
