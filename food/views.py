from django.http import Http404
from django.shortcuts import get_object_or_404
from food.models import Food, FoodCategory
from django.views.generic import DetailView, ListView

class FoodDetailView(DetailView):
	queryset = Food.objects.all()

	def get_object(self):
		object = super(FoodDetailView, self).get_object();

		object.view_num = object.view_num + 1
		object.save()

		return object


class FoodCategoryListView(ListView):
	context_object_name = "food_list"
	paginate_by = 10

	def get_queryset(self):
		if self.args[1] == 'hot':
			self.foodcategory = get_object_or_404(FoodCategory, id__iexact=self.args[0])
			return Food.objects.filter(category = self.foodcategory)
		elif self.args[1] == 'time':
			self.foodcategory = get_object_or_404(FoodCategory, id__iexact=self.args[0])
			return Food.objects.filter(category = self.foodcategory).order_by("date")
		elif self.args[1] == 'trend':
			self.foodcategory = get_object_or_404(FoodCategory, id__iexact=self.args[0])
			return Food.objects.filter(category = self.foodcategory).order_by("-trend_num")
		else:
			raise Http404

	def get_context_data(self, **kwargs):
		context = super(FoodCategoryListView, self).get_context_data(**kwargs)
		context['category'] = self.foodcategory
		context['category_list'] = FoodCategory.objects.all()
		return context


