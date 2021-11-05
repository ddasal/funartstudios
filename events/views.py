from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .forms import EventForm, EventStaffForm, EventCustomerForm
from.models import Event, EventCustomer, EventStaff

# Create your views here.

@permission_required('events.view_event')
def event_list_view(request):
    qs = Event.objects.filter(active=True).order_by('-date', '-time')
    page = request.GET.get('page', 1)

    paginator = Paginator(qs, 10)
    event_count = paginator.count
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    context = {
        "events": events,
        "event_count": event_count
    }
    return render(request, "events/list.html", context)

@permission_required('events.view_event')
def event_detail_view(request, slug=None):
    hx_url = reverse("events:hx-detail", kwargs={"slug": slug})
    event_obj = Event.objects.get(slug=slug)
    context = {
        "hx_url": hx_url,
        "event_obj": event_obj
    }
    return render(request, "events/detail.html", context)



@permission_required('events.delete_event')
def event_delete_view(request, slug=None):
    try:
        obj = Event.objects.get(slug=slug)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse('Not f=Found')
        raise Http404
    if request.method == "POST":
        obj.delete()
        success_url = reverse('events:list')
        if request.htmx:
            headers = {
                "HX-Redirect": success_url
            }
            return HttpResponse('Success', headers=headers)
        return redirect(success_url)
    context = {
        "object": obj
    }
    return render(request, "events/delete.html", context)

@permission_required('events.delete_eventstaff')
def event_staff_delete_view(request, parent_slug=None, id=None):
    print(id)
    try:
        obj = EventStaff.objects.get(event__slug=parent_slug, id=id)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse('Not found')
        raise Http404
    if request.method == "POST":
        staff = obj.user
        obj.delete()
        success_url = reverse('events:detail', kwargs={"slug": parent_slug})
        if request.htmx:
            return render(request, "events/partials/staff-inline-delete-response.html", {"staff": staff})
        return redirect(success_url)
    context = {
        "object": obj
    }
    return render(request, "events/delete.html", context)


@permission_required('events.delete_eventcustomer')
def event_customer_delete_view(request, parent_slug=None, id=None):
    print(id)
    try:
        obj = EventCustomer.objects.get(event__slug=parent_slug, id=id)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse('Not found')
        raise Http404
    if request.method == "POST":
        customer = obj
        obj.delete()
        success_url = reverse('events:detail', kwargs={"slug": parent_slug})
        if request.htmx:
            return render(request, "events/partials/customer-inline-delete-response.html", {"customer": customer})
        return redirect(success_url)
    context = {
        "object": obj
    }
    return render(request, "events/delete.html", context)



@permission_required('events.view_event')
def event_detail_hx_view(request, slug=None):
    if not request.htmx:
        raise Http404
    try:
        obj = Event.objects.get(slug=slug)
        new_staff_url = reverse("events:hx-staff-create", kwargs={"parent_slug": obj.slug})
        new_customer_url = reverse("events:hx-customer-create", kwargs={"parent_slug": obj.slug})
    except:
        obj = None
    if obj is None:
        return HttpResponse("Not found.")
    context = {
        "object": obj,
        "new_staff_url": new_staff_url,
        "new_customer_url": new_customer_url
    }
    return render(request, "events/partials/detail.html", context)
 


@permission_required('events.add_event')
def event_create_view(request):
    form = EventForm(request.POST or None)
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
    return render(request, "events/create-update.html", context) 

@permission_required('events.change_event')
def event_update_view(request, slug=None):
    obj = get_object_or_404(Event, slug=slug)
    form = EventForm(request.POST or None, instance=obj)
    new_staff_url = reverse("events:hx-staff-create", kwargs={"parent_slug": obj.slug})
    new_customer_url = reverse("events:hx-customer-create", kwargs={"parent_slug": obj.slug})
    context = {
        "form": form,
        "object": obj,
        "new_staff_url": new_staff_url,
        "new_customer_url": new_customer_url
    }
    if form.is_valid():
        form.save()
        context['message'] = 'Event data saved.'
    if request.htmx:
        return render(request, "events/partials/forms.html", context)
    return render(request, "events/create-update.html", context) 


@permission_required('events.change_eventstaff')
def event_staff_update_hx_view(request, parent_slug=None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_obj = Event.objects.get(slug=parent_slug)
    except:
        parent_obj = None
    if parent_obj is None:
        return HttpResponse("Not found.")

    instance = None
    if id is not None:
        try:
            instance = EventStaff.objects.get(event=parent_obj, id=id)
        except:
            instance = None
    form = EventStaffForm(request.POST or None, instance=instance)
    url = reverse("events:hx-staff-create", kwargs={"parent_slug": parent_obj.slug})
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
            new_obj.event = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, "events/partials/staff-inline.html", context)
    
    return render(request, "events/partials/staff-form.html", context)




@permission_required('events.change_eventcustomer')
def event_customer_update_hx_view(request, parent_slug=None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_obj = Event.objects.get(slug=parent_slug)
    except:
        parent_obj = None
    if parent_obj is None:
        return HttpResponse("Not found.")

    instance = None
    if id is not None:
        try:
            instance = EventCustomer.objects.get(event=parent_obj, id=id)
        except:
            instance = None
    form = EventCustomerForm(request.POST or None, instance=instance)
    url = reverse("events:hx-customer-create", kwargs={"parent_slug": parent_obj.slug})
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
            new_obj.event = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, "events/partials/customer-inline.html", context)
    
    return render(request, "events/partials/customer-form.html", context)

