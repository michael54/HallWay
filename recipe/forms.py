from django.forms import ModelForm
from recipe.models import Recipe, Step, Vote, DidRecipe, RecipeCategory
from django.forms.models import inlineformset_factory
from django import forms
from django.conf import settings
import os
import sys

class DidRecipeForm(ModelForm):
	class Meta:
		model = DidRecipe
		exclude = ('date', )
		widgets = {
			'recipe': forms.HiddenInput(),
			'user': forms.HiddenInput(),
		}

class RecipeForm(ModelForm):
	prep_time = forms.TimeField(input_formats=['%H:%M','%H:%M:%S',])
	cook_time = forms.TimeField(input_formats=['%H:%M','%H:%M:%S',])
	cover_image = forms.CharField(widget=forms.HiddenInput(), required=False)
	class Meta:
		model = Recipe
		fields = ('name', 'author', 'category', 'brief', 'cover_image', 'tips', 'prep_time', 'cook_time')
		widgets = {
			'author': forms.HiddenInput(),
		}

class VoteForm(forms.Form):
	score = forms.IntegerField(min_value = 0, max_value = 5)
	comment = forms.CharField(widget=forms.Textarea, required=False)

class StepForm(forms.Form):
	description = forms.CharField(widget=forms.Textarea(), min_length = 1)
	step_image = forms.CharField(widget=forms.HiddenInput(), required=False)

class AmountForm(forms.Form):
	ingredient = forms.CharField(min_length = 1)
	amount = forms.CharField(min_length = 1)
	must = forms.BooleanField(required=False)

class SearchForm(forms.Form):
	ingredient = forms.CharField(min_length = 1)


MIN_RATING_CHOICES=(
	('0', '0'),
	('1', '1'),
	('2', '2'),
	('3', '3'),
	('4', '4'),
	('5', '5'),
)
COURSES_CHOICES =[('0', 'None'),] + [ (obj.id, obj.name) for obj in list(RecipeCategory.objects.filter(parent__name='Courses').only('name'))]
CUISINES_CHOICES =[('0', 'None'),] + [ (obj.id, obj.name) for obj in list(RecipeCategory.objects.filter(parent__name='Cuisines').only('name'))]
INGREDIENTS_CHOICES =[('0', 'None'),] + [ (obj.id, obj.name) for obj in list(RecipeCategory.objects.filter(parent__name='Main Ingredients').only('name'))]
DIETS_CHOICES =[('0', 'None'),] + [ (obj.id, obj.name) for obj in list(RecipeCategory.objects.filter(parent__name='Special Diets').only('name'))]

class SearchFormExtra(forms.Form):
	courses = forms.ChoiceField(choices=COURSES_CHOICES)
	cuisines = forms.ChoiceField(choices=CUISINES_CHOICES)
	main_ingredients = forms.ChoiceField(choices=INGREDIENTS_CHOICES)
	special_diets = forms.ChoiceField(choices=DIETS_CHOICES)
	min_rating = forms.ChoiceField(choices=MIN_RATING_CHOICES)


