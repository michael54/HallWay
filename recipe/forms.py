from django.forms import ModelForm
from recipe.models import Recipe, Step, Vote
from django.forms.models import inlineformset_factory
from django import forms
from django.conf import settings
import os
import sys

class RecipeForm(ModelForm):
	prep_time = forms.TimeField(input_formats=['%H:%M','%H:%M:%S',])
	cook_time = forms.TimeField(input_formats=['%H:%M','%H:%M:%S',])
	cover_image = forms.CharField(required=False)
	class Meta:
		model = Recipe
		fields = ('name', 'author', 'category', 'brief', 'cover_image', 'tips', 'prep_time', 'cook_time')
		widgets = {
			'author': forms.HiddenInput(),
		}

	def save(self, force_insert=False, force_update=False, commit=True):
		if self.instance:
			print >> sys.stderr, self.instance.cover_image
			if self.instance.cover_image != self.cleaned_data['cover_image']:
				self.instance.cover_image.delete()

		m = super(RecipeForm, self).save(commit=False)
		
		if commit:
			m.save()
		return m

class VoteForm(forms.Form):
	score = forms.IntegerField(min_value = 0, max_value = 5)
	comment = forms.CharField(widget=forms.Textarea)

class StepForm(forms.Form):
	description = forms.CharField(min_length = 1)
	step_image = forms.CharField(required=False)

class AmountForm(forms.Form):
	ingredient = forms.CharField(min_length = 1)
	amount = forms.CharField(min_length = 1)
	must = forms.BooleanField()


