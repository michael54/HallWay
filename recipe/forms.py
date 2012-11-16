from django.forms import ModelForm
from recipe.models import Recipe, Step, Vote
from django.forms.models import inlineformset_factory
from django import forms

class RecipeForm(forms.Form):
	name = forms.CharField()
	category = forms.CharField()
	brief = forms.CharField(widget=forms.Textarea)
	cover_image = forms.ImageField()
	tips = forms.CharField(widget=forms.Textarea)
	prep_time = forms.TimeField(input_formats='%H:%M')
	cook_time = forms.TimeField(input_formats='%H:%M')

class VoteForm(forms.Form):
	score = forms.IntegerField(min_value = 0, max_value = 5)
	comment = forms.CharField(widget=forms.Textarea)

class StepForm(forms.Form):
	step_num = forms.IntegerField(min_value = 1)
	description = forms.CharField()
	step_image = forms.ImageField(required=False)

class AmountForm(forms.Form):
	ingredient = forms.CharField()
	amount = forms.CharField()
	must = forms.BooleanField()


