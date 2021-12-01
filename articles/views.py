from django.contrib.auth.decorators import permission_required, login_required
from django.http import Http404
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse
from .models import Article, ArticleManager, Comment
from .forms import ArticleForm, CommentForm

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
        article_object = form.save(commit=False)
        article_object.user = request.user
        article_object.save()
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
        new_comment_url = reverse("articles:hx-comment-create", kwargs={"parent_slug": obj.slug})
        view_count = obj.page_views + int(1)
        requester = request.user.first_name + ' ' + request.user.last_name
        if obj.seen_by is None:
            obj.seen_by = requester
        elif requester not in obj.seen_by:
            add_requester = obj.seen_by + ', ' + requester
            obj.seen_by = add_requester

        obj.page_views = view_count
        obj.save()
    except:
        obj = None
    if obj is None:
        return HttpResponse("Not found.")
    context = {
        "object": obj,
        "new_comment_url": new_comment_url
    }
    return render(request, "articles/partials/detail.html", context)


@permission_required('articles.change_article')
def article_update_view(request, slug=None):
    obj = get_object_or_404(Article, slug=slug)
    form = ArticleForm(request.POST or None, instance=obj)
    new_comment_url = reverse("articles:hx-comment-create", kwargs={"parent_slug": obj.slug})
    context = {
        "form": form,
        "object": obj,
        "new_comment_url": new_comment_url
    }
    if form.is_valid():
        form.save()
        context['message'] = 'Article data saved.'
    if request.htmx:
        return render(request, "articles/partials/forms.html", context)
    return render(request, "articles/create-update.html", context) 


@permission_required('articles.delete_comment')
def article_comment_delete_view(request, parent_slug=None, id=None):
    try:
        obj = Comment.objects.get(article__slug=parent_slug, id=id)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse('Not found')
        raise Http404
    if request.method == "POST":
        commenter = obj.user
        obj.delete()
        success_url = reverse('articles:detail', kwargs={"slug": parent_slug})
        if request.htmx:
            return render(request, "articles/partials/comment-inline-delete-response.html", {"commenter": commenter})
        return redirect(success_url)

    context = {
        "object": obj
    }
    return render(request, "articles/delete.html", context)

@permission_required('articles.change_comment')
def article_comment_update_hx_view(request, parent_slug=None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_obj = Article.objects.get(slug=parent_slug)
    except:
        parent_obj = None
    if parent_obj is None:
        return HttpResponse("Not found.")
 
    instance = None
    if id is not None:
        try:
            instance = Comment.objects.get(article=parent_obj, id=id)
        except:
            instance = None
    form = CommentForm(request.POST or None, instance=instance)
    url = reverse("articles:hx-comment-create", kwargs={"parent_slug": parent_obj.slug})
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
            new_obj.article = parent_obj
            new_obj.user = request.user
        new_obj.save()
        context['object'] = new_obj
        return render(request, "articles/partials/comment-inline.html", context)
    
    return render(request, "articles/partials/comment-form.html", context)

