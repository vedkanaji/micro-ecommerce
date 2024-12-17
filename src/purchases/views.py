from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
# Create your views here.
from products.models import Product
from purchases.models import Purchase

def purchase_start_view(request):
    if not request.method == 'POST':
        return HttpResponseBadRequest()
    if not request.user.is_authenticated():
        return HttpResponseBadRequest()
    handle = request.POST.get('handle')
    product = get_object_or_404(Product, handle=handle)
    purchase = Purchase.objects.create(product=product, user=request.user)
    request.session['purchase_id'] = purchase.id
    return HttpResponse("Start purchase")

def purchase_success_view(request):
    purchase_id = request.session.get('purchase_id')
    if purchase_id:
        purchase = Purchase.objects.get(id=purchase_id)
        purchase.completed = True
        purchase.save()
    return HttpResponse(f'finished purchase {purchase_id}')