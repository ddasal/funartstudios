from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .forms import ProductForm, PurchaseItemForm, PurchaseOrderForm
from.models import Product, PurchaseItem, PurchaseOrder

# Create your views here.

@permission_required('products.view_product')
def product_list_view(request):
    qs = Product.objects.all().order_by('type', 'name')
    page = request.GET.get('page', 1)

    paginator = Paginator(qs, 10)
    product_count = paginator.count
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {
        "products": products,
        "product_count": product_count
    }
    return render(request, "products/list.html", context)

@permission_required('products.view_product')
def product_detail_view(request, slug=None):
    hx_url = reverse("products:hx-detail", kwargs={"slug": slug})
    product_obj = Product.objects.get(slug=slug)
    context = {
        "hx_url": hx_url,
        "product_obj": product_obj
    }
    return render(request, "products/detail.html", context)



@permission_required('products.delete_product')
def product_delete_view(request, slug=None):
    try:
        obj = Product.objects.get(slug=slug)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse('Not f=Found')
        raise Http404
    if request.method == "POST":
        obj.delete()
        success_url = reverse('products:list')
        if request.htmx:
            headers = {
                "HX-Redirect": success_url
            }
            return HttpResponse('Success', headers=headers)
        return redirect(success_url)
    context = {
        "object": obj
    }
    return render(request, "products/delete.html", context)



@permission_required('products.view_product')
def product_detail_hx_view(request, slug=None):
    if not request.htmx:
        raise Http404
    try:
        obj = Product.objects.get(slug=slug)
    except:
        obj = None
    if obj is None:
        return HttpResponse("Not found.")
    context = {
        "object": obj
    }
    return render(request, "products/partials/detail.html", context)
 


@permission_required('products.add_product')
def product_create_view(request):
    form = ProductForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        success_url = reverse('products:list')
        if request.htmx:
            headers = {
                "HX-Redirect": success_url
            }
            return HttpResponse('Created', headers=headers)
        return redirect(obj.get_absolute_url())
    return render(request, "products/create-update.html", context) 

@permission_required('products.change_product')
def product_update_view(request, slug=None):
    obj = get_object_or_404(Product, slug=slug)
    form = ProductForm(request.POST or None, instance=obj)
    context = {
        "form": form,
        "object": obj
    }
    if form.is_valid():
        form.save()
        context['message'] = 'Product data saved.'
    if request.htmx:
        return render(request, "products/partials/forms.html", context)
    return render(request, "products/create-update.html", context) 





# purchase order views


@permission_required('products.view_purchaseorder')
def po_list_view(request):
    qs = PurchaseOrder.objects.all().order_by('-date')
    page = request.GET.get('page', 1)

    paginator = Paginator(qs, 10)
    po_count = paginator.count
    try:
        pos = paginator.page(page)
    except PageNotAnInteger:
        pos = paginator.page(1)
    except EmptyPage:
        pos = paginator.page(paginator.num_pages)
    context = {
        "pos": pos,
        "po_count": po_count
    }
    return render(request, "products/po-list.html", context)

@permission_required('products.view_purchaseorder')
def po_detail_view(request, id=None):
    hx_url = reverse("products:hx-po-detail", kwargs={"id": id})
    po_obj = PurchaseOrder.objects.get(id=id)
    context = {
        "hx_url": hx_url,
        "po_obj": po_obj
    }
    return render(request, "products/po-detail.html", context)



@permission_required('products.delete_purchaseorder')
def po_delete_view(request, id=None):
    try:
        obj = PurchaseOrder.objects.get(id=id)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse('Not found')
        raise Http404
    if request.method == "POST":
        obj.delete()
        success_url = reverse('products:po-list')
        if request.htmx:
            headers = {
                "HX-Redirect": success_url
            }
            return HttpResponse('Success', headers=headers)
        return redirect(success_url)
    context = {
        "object": obj
    }
    return render(request, "products/po-delete.html", context)

@permission_required('products.delete_purchaseitem')
def po_item_delete_view(request, parent_id=None, id=None):
    try:
        obj = PurchaseItem.objects.get(purchase_order__id=parent_id, id=id)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse('Not found')
        raise Http404
    if request.method == "POST":
        item = obj.product
        obj.delete()
        success_url = reverse('products:po-detail', kwargs={"id": parent_id})
        if request.htmx:
            return render(request, "products/partials/item-inline-delete-response.html", {"item": item})
        return redirect(success_url)
    context = {
        "object": obj
    }
    return render(request, "products/po-delete.html", context)


@permission_required('products.view_purchaseorder')
def po_detail_hx_view(request, id=None):
    if not request.htmx:
        raise Http404
    try:
        obj = PurchaseOrder.objects.get(id=id)
        new_item_url = reverse("products:hx-po-item-create", kwargs={"parent_id": obj.id})
    except:
        obj = None
    if obj is None:
        return HttpResponse("Not found.")
    context = {
        "object": obj,
        "new_item_url": new_item_url
    }
    return render(request, "products/partials/po-detail.html", context)
 


@permission_required('products.add_purchaseorder')
def po_create_view(request):
    form = PurchaseOrderForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        if request.htmx:
            headers = {
                "HX-Redirect": obj.get_absolute_url()
            }
            return HttpResponse('Created', headers=headers)
        return redirect(obj.get_absolute_url())
    return render(request, "products/po-create-update.html", context) 

@permission_required('products.change_purchaseorder')
def po_update_view(request, id=None):
    obj = get_object_or_404(PurchaseOrder, id=id)
    form = PurchaseOrderForm(request.POST or None, instance=obj)
    new_item_url = reverse("products:hx-po-item-create", kwargs={"parent_id": obj.id})
    context = {
        "form": form,
        "object": obj,
        "new_item_url": new_item_url
    }
    if form.is_valid():
        form.save()
        context['message'] = 'Purchase Order data saved.'
    if request.htmx:
        return render(request, "products/partials/po-forms.html", context)
    return render(request, "products/po-create-update.html", context) 


@permission_required('products.change_purchaseitem')
def po_item_update_hx_view(request, parent_id=None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_obj = PurchaseOrder.objects.get(id=parent_id)
    except:
        parent_obj = None
    if parent_obj is None:
        return HttpResponse("Not found.")

    instance = None
    if id is not None:
        try:
            instance = PurchaseItem.objects.get(purchase_order=parent_obj, id=id)
        except:
            instance = None
    form = PurchaseItemForm(request.POST or None, instance=instance)
    url = reverse("products:hx-po-item-create", kwargs={"parent_id": parent_obj.id})
    if instance:
        url = instance.get_htmx_edit_url()        
    
    context = {
        "url": url,
        "form": form,
        "object": instance
    }
    if form.is_valid():
        new_obj = form.save(commit=False)
        if instance is None:
            new_obj.purchase_order = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, "products/partials/item-inline.html", context)
    
    return render(request, "products/partials/item-form.html", context)

