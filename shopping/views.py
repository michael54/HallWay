from django.views.generic.detail import DetailView
from shopping.models import ShoppingList
from recipe.models import Amount
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
import json
import sys

def view_shopping_list(request):
	if request.session.get('shopping_list'):
		sl_id = request.session.get('shopping_list')
		try :
			sl = ShoppingList.objects.get(id = sl_id)
		except ShoppingList.DoesNotExist:
			sl = ShoppingList()
			sl.save()
			request.session['shopping_list'] = sl.id
		l = list(sl.amount.all())
	else:
		l = list()
	return render(request, 'shopping/shoppinglist_detail.html', {'amount_list': l})


def add_item(request):
	""" Add an ingredient with amount into shopping list """
	if request.is_ajax() and request.method == 'POST':
		amount_id = int(request.POST['amount'])
		amount_item = get_object_or_404(Amount, pk=amount_id)

		if request.session.get('shopping_list'):
			sl_id = request.session.get('shopping_list')
			try :
				sl = ShoppingList.objects.get(id = sl_id)
			except ShoppingList.DoesNotExist:
				sl = ShoppingList()
				sl.save()
				request.session['shopping_list'] = sl.id
			sl.amount.add(amount_item)
		else:
			sl = ShoppingList()
			sl.save()
			sl.amount.add(amount_item)
			request.session['shopping_list'] = sl.id
		return HttpResponse(json.dumps({'success': 'true'}), mimetype="application/json")
	else:
		raise Http404




