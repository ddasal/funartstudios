from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .forms import ProductForm
from.models import Product

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

