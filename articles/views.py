from django.contrib.auth.decorators import permission_required, login_required
from django.http import Http404
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse
from .models import Article, ArticleManager
from .forms import ArticleForm

# Create your views here.

def article_search_view(request):
    query = request.GET.get('q')
    qs = Article.objects.search(query=query)
    context = {
        "object_list": qs,        
    }
    return render(request, "articles/search.html", context=context)


@login_required
def article_create_view(request, id=None):
    form = ArticleForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        article_object = form.save()
        context['form'] = ArticleForm()
        context['object'] = article_object
        context['created'] = True
        return redirect(article_object.get_absolute_url())

    return render(request, "articles/create.html", context=context)


@permission_required('articles.view_article')
def article_detail_view(request, slug=None):
    hx_url = reverse("articles:hx-detail", kwargs={"slug": slug})
    article_obj = Article.objects.get(slug=slug)
    context = {
        "hx_url": hx_url,
        "article_obj": article_obj
    }
    return render(request, "articles/detail.html", context)

@permission_required('articles.delete_article')
def article_delete_view(request, slug=None):
    try:
        obj = Article.objects.get(slug=slug)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse('Not found')
        raise Http404
    if request.method == "POST":
        obj.delete()
        success_url = reverse('home')
        if request.htmx:
            headers = {
                "HX-Redirect": success_url
            }
            return HttpResponse('Success', headers=headers)
        return redirect(success_url)
    context = {
        "object": obj
    }
    return render(request, "articles/delete.html", context)

@permission_required('articles.view_article')
def article_detail_hx_view(request, slug=None):
    if not request.htmx:
        raise Http404
    try:
        obj = Article.objects.get(slug=slug)
    except:
        obj = None
    if obj is None:
        return HttpResponse("Not found.")
    context = {
        "object": obj
    }
    return render(request, "articles/partials/detail.html", context)

@permission_required('articles.change_article')
def article_update_view(request, slug=None):
    obj = get_object_or_404(Article, slug=slug)
    form = ArticleForm(request.POST or None, instance=obj)
    context = {
        "form": form,
        "object": obj
    }
    if form.is_valid():
        form.save()
        context['message'] = 'Article data saved.'
    if request.htmx:
        return render(request, "articles/partials/forms.html", context)
    return render(request, "articles/create-update.html", context) 
