from shopping.models import ShoppingList
from recipe.models import Amount
from django.shortcuts import get_object_or_404

def add_item(request):
	""" Add an ingredient with amount into shopping list """
	if request.is_ajax() and request.method=="POST":
		amount = get_object_or_404(Amount, pk=int(request.POST['amount']))
		if request.session.get('shopping_list',False):
			sl = ShoppingList.objects.get(id=request.session['shopping_list'])
		else:
			sl = ShoppingList()
			sl.save()
		sl.amount.add(amount)
		sl.save()




