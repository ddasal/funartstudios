from django.contrib.auth.decorators import permission_required, login_required
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse
from .models import Faq, FaqManager
from .forms import FaqForm
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.

@permission_required('faq.view_faq')
def faq_list_view(request, *args, **kwargs): 
    if request.method == "POST":
        query = request.POST.get('q')
        lookups = Q(question__icontains=query) | Q(answer__icontains=query)  
        qs = Faq.objects.filter(lookups).order_by('category').distinct()
    else:
        qs = Faq.objects.all().order_by('category')
        query = ''
    page = request.GET.get('page', 1)
    paginator = Paginator(qs, 100)
    faq_count = paginator.count
    try:
        faq = paginator.page(page)
    except PageNotAnInteger:
        faq = paginator.page(1)
    except EmptyPage:
        faq = paginator.page(paginator.num_pages)

    context = {
        "faq": faq,
        "faq_count": faq_count,
        "q": query,
    }
    return render(request, 'faq/list.html', context)

@permission_required('faq.view_faq')
def faq_search_view(request):
    query = request.GET.get('q')
    qs = Faq.objects.search(query=query)
    context = {
        "object_list": qs,        
    }
    return render(request, "faq/search.html", context=context)


@permission_required('faq.add_faq')
def faq_create_view(request, id=None):
    form = FaqForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        faq_object = form.save(commit=False)
        faq_object.user = request.user
        faq_object.save()
        faq_object = form.save()
        context['form'] = FaqForm()
        context['object'] = faq_object
        context['created'] = True
        #return redirect(faq_object.get_absolute_url())
        return redirect('faq:list')

    return render(request, "faq/create.html", context=context)


@permission_required('faq.view_faq')
def faq_detail_view(request, slug=None):
    hx_url = reverse("faq:hx-detail", kwargs={"slug": slug})
    faq_obj = Faq.objects.get(slug=slug)
    context = {
        "hx_url": hx_url,
        "faq_obj": faq_obj
    }
    return render(request, "faq/detail.html", context)

@permission_required('faq.delete_faq')
def faq_delete_view(request, slug=None):
    try:
        obj = Faq.objects.get(slug=slug)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse('Not found')
        raise Http404
    if request.method == "POST":
        obj.delete()
        success_url = reverse('faq:list')
        if request.htmx:
            headers = {
                "HX-Redirect": success_url
            }
            return HttpResponse('Success', headers=headers)
        return redirect(success_url)
    context = {
        "object": obj
    }
    return render(request, "faq/delete.html", context)

@permission_required('faq.view_faq')
def faq_detail_hx_view(request, slug=None):
    if not request.htmx:
        raise Http404
    try:
        obj = Faq.objects.get(slug=slug)
        view_count = obj.page_views + int(1)
        obj.page_views = view_count
        obj.save()
    except:
        obj = None
    if obj is None:
        return HttpResponse("Not found.")
    context = {
        "object": obj,
    }
    return render(request, "faq/partials/detail.html", context)


@permission_required('faq.change_faq')
def faq_update_view(request, slug=None):
    obj = get_object_or_404(Faq, slug=slug)
    form = FaqForm(request.POST or None, instance=obj)
    context = {
        "form": form,
        "object": obj,
    }
    if form.is_valid():
        form.save()
        context['message'] = 'FAQ data saved.'
    if request.htmx:
        return render(request, "faq/partials/forms.html", context)
    return render(request, "faq/create-update.html", context) 
