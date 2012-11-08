from django.shortcuts import get_object_or_404
from food.models import Food
from django.views.generic import DetailView

class FoodDetailView(DetailView):
	queryset = Food.objects.all()

	def get_object(self):
		object = super(FoodDetailView, self).get_object();

		object.view_num = object.view_num + 1
		object.save()

		return object
