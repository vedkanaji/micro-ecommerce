import mimetypes

from django.http import FileResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, ProductAttachment
from .forms import ProductForm, ProductUpdateForm, ProductAttachmentInLineFormSet


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
    attachment = ProductAttachment.objects.filter(product=product)
    is_owner = False
    if request.user.is_authenticated:
        is_owner = request.user.purchase_set.filter(product=product, completed=True).exists()
    context = {'product': product, 'is_owner': is_owner, 'attachment': attachment}
    return render(request, 'products/detail.html', context)


def product_manage_detail_view(request, handle=None):
    obj = get_object_or_404(Product, handle=handle)
    attachments = ProductAttachment.objects.filter(product=obj)
    is_manager = False
    if request.user.is_authenticated:
        is_manager = obj.user == request.user
    context = {"object": obj}
    if not is_manager:
        return HttpResponseBadRequest()
    form = ProductUpdateForm(request.POST or None, request.FILES or None, instance=obj)
    formset = ProductAttachmentInLineFormSet(request.POST or None, 
                                             request.FILES or None,queryset=attachments)
    if form.is_valid() and formset.is_valid():
        instance = form.save(commit=False)
        instance.save()
        formset.save(commit=False)
        for _form in formset:
            is_delete = _form.cleaned_data.get("DELETE")
            try:
                attachment_obj = _form.save(commit=False)
            except:
                attachment_obj = None
            if is_delete:
                if attachment_obj is not None:
                    if attachment_obj.pk:
                        attachment_obj.delete()
            else:
                if attachment_obj is not None:
                    attachment_obj.product  = instance
                    attachment_obj.save()
        return redirect(obj.get_manage_url())
    context['form'] = form
    context['formset'] = formset
    return render(request, 'products/manager.html', context)

def product_attachment_download_view(request, handle=None, pk=None):
    attachment = get_object_or_404(ProductAttachment, product__handle=handle, pk=pk)
    can_download = attachment.is_free or False
    if request.user.is_authenticated:
        can_download = True
    if can_download is False:
        return HttpResponseBadRequest()
    file = attachment.file.open(mode='rb')
    filename = attachment.file.name
    response = FileResponse(file)
    response['Content-type'] = mimetypes.guess_type(filename)[0]
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
