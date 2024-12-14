import mimetypes

from django.http import FileResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm, ProductUpdateForm

def product_view(request):
    context = {}
    form = ProductForm(request.POST or None)  
    if form.is_valid():
        obj = form.save(commit=False)
        if request.user.is_authenticated:
            obj.user = request.user  
            obj.save()
            return redirect('products/create.html')  
        else:
            form.add_error(None, 'User is not authenticated') 
    
    context['form'] = form
    return render(request, 'products/create.html', context) 

def product_list_view(request):
    products = Product.objects.all()
    return render(request, 'products/list.html', {'products': products})

def product_detail_view(request, handle=None):
    product = get_object_or_404(Product, handle=handle)
    is_owner = request.user.is_authenticated and product.user == request.user
    context = {'product': product, 'is_owner': is_owner}
    if is_owner:
        form = ProductUpdateForm(request.POST or None, request.FILES or None, instance=product)  
        if request.method == 'POST' and form.is_valid():
            form.save() 
            return redirect('products:detail', handle=product.handle)  
        context['form'] = form 
    else:
        context['form'] = None 
    
    return render(request, 'products/detail.html', context)


# def product_attachment_download(request, handle=None):