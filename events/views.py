from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .forms import EventForm, EventStaffForm, EventCustomerForm, EventTipForm
from.models import Event, EventCustomer, EventStaff, EventTip
from royaltyreports.models import RoyaltyReport

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
        "event_count": event_count,
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
            return HttpResponse('Not found')
        raise Http404
    if request.method == "POST":
        if obj.status == 'p':
            obj.delete()
            success_url = reverse('events:list')
            if request.htmx:
                headers = {
                    "HX-Redirect": success_url
                }
                return HttpResponse('Success', headers=headers)
            return redirect(success_url)
        else:
            success_url = reverse('events:list')
            if request.htmx:
                headers = {
                    "HX-Redirect": success_url,
                }
                return HttpResponse('Success', headers=headers)
            return redirect(success_url)

    context = {
        "object": obj
    }
    return render(request, "events/delete.html", context)

@permission_required('events.delete_eventstaff')
def event_staff_delete_view(request, parent_slug=None, id=None):
    try:
        obj = EventStaff.objects.get(event__slug=parent_slug, id=id)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse('Not found')
        raise Http404
    if request.method == "POST":
        if obj.status == 'p':
            staff = obj.user
            obj.delete()
            success_url = reverse('events:detail', kwargs={"slug": parent_slug})
            if request.htmx:
                return render(request, "events/partials/staff-inline-delete-response.html", {"staff": staff})
            return redirect(success_url)
        else:
            message = "Unable to delete."
            success_url = reverse('events:detail', kwargs={"slug": parent_slug})
            if request.htmx:
                return render(request, "events/partials/staff-inline-delete-response.html", {"message": message})
            return redirect(success_url)

    context = {
        "object": obj
    }
    return render(request, "events/delete.html", context)


@permission_required('events.delete_eventcustomer')
def event_customer_delete_view(request, parent_slug=None, id=None):
    try:
        obj = EventCustomer.objects.get(event__slug=parent_slug, id=id)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse('Not found')
        raise Http404
    if request.method == "POST":
        if obj.status == 'p':
            customer = obj
            obj.delete()
            success_url = reverse('events:detail', kwargs={"slug": parent_slug})
            if request.htmx:
                return render(request, "events/partials/customer-inline-delete-response.html", {"customer": customer})
            return redirect(success_url)
        else:
            message = "Unable to delete."
            success_url = reverse('events:detail', kwargs={"slug": parent_slug})
            if request.htmx:
                return render(request, "events/partials/customer-inline-delete-response.html", {"message": message})
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
        new_tip_url = reverse("events:hx-tip-create", kwargs={"parent_slug": obj.slug})
    except:
        obj = None
    if obj is None:
        return HttpResponse("Not found.")
    context = {
        "object": obj,
        "new_staff_url": new_staff_url,
        "new_customer_url": new_customer_url,
        "new_tip_url": new_tip_url
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
        royalty_date_check = RoyaltyReport.objects.filter(end_date__gte=obj.date, start_date__lte=obj.date, status='c')
        if royalty_date_check:
            return HttpResponse("Unable to create event. Check that your date isn't conflicting with a closed Pay Period or Royalty Report.")
        else:
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
    new_tip_url = reverse("events:hx-tip-create", kwargs={"parent_slug": obj.slug})
    context = {
        "form": form,
        "object": obj,
        "new_staff_url": new_staff_url,
        "new_customer_url": new_customer_url,
        "new_tip_url": new_tip_url
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



@permission_required('events.change_eventtip')
def event_tip_update_hx_view(request, parent_slug=None, id=None):
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
            instance = EventTip.objects.get(event=parent_obj, id=id)
        except:
            instance = None
    form = EventTipForm(request.POST or None, instance=instance)
    url = reverse("events:hx-tip-create", kwargs={"parent_slug": parent_obj.slug})
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
        return render(request, "events/partials/tip-inline.html", context)
    
    return render(request, "events/partials/tip-form.html", context)

@permission_required('events.delete_eventtip')
def event_tip_delete_view(request, parent_slug=None, id=None):
    try:
        obj = EventTip.objects.get(event__slug=parent_slug, id=id)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse('Not found')
        raise Http404
    if request.method == "POST":
        if obj.status == 'p':
            tip = obj.tip_amount
            obj.delete()
            success_url = reverse('events:detail', kwargs={"slug": parent_slug})
            if request.htmx:
                return render(request, "events/partials/tip-inline-delete-response.html", {"tip": tip})
            return redirect(success_url)
        else:
            message = "Unable to delete."
            success_url = reverse('events:detail', kwargs={"slug": parent_slug})
            if request.htmx:
                return render(request, "events/partials/tip-inline-delete-response.html", {"message": message})
            return redirect(success_url)

    context = {
        "object": obj
    }
    return render(request, "events/delete.html", context)



from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from datetime import datetime
from django.views import View
from .models import EventStaff
import io,csv

# @login_required
class EventStaffUpload(View):
    def get(self, request):
        template_name = 'events/import-staff.html'
        return render(request, template_name)
    def post(self, request):
        user = request.user #get the current login user details
        paramFile = io.TextIOWrapper(request.FILES['eventstaff'].file)
        portfolio1 = csv.DictReader(paramFile)
        list_of_dict = list(portfolio1)
        objs = [
            EventStaff(
            role=row['role'],
            hours=row['hours'],
            event_id=row['event_id'],
            user_id=row['new_user_id'],
            event_qty=row['event_qty'],
            # prepaint_qty=row['prepaint_qty'],
            event_product_id=row['event_product'],
            # prepaint_product_id=row['prepaint_product'],
         )
         for row in list_of_dict
     ]
        try:
            msg = EventStaff.objects.bulk_create(objs)
            returnmsg = {"status_code": 200}
            print('imported successfully')
        except Exception as e:
            print('Error While Importing Data: ',e)
            returnmsg = {"status_code": 500}
       
        return JsonResponse(returnmsg)


from decimal import Decimal

# @permission_required('square.add_square')
class EventCustomerUpload(View):
    def get(self, request):
        template_name = 'events/import-eventcustomers.html'
        return render(request, template_name)

    def post(self, request):
        user = request.user #get the current login user details
        paramFile = io.TextIOWrapper(request.FILES['eventfile'].file)
        portfolio1 = csv.DictReader(paramFile)
        list_of_dict = list(portfolio1)
        objs = [
            EventCustomer(
                type='r',
                quantity=row['surface_qty'],
                event_id=row['event_id'],
                per_customer_qty='1',
                product_id=row['surface_id'],
                price=row['surface_price'],
                status='c',
            )
            for row in list_of_dict
        ]
        try:
            msg = EventCustomer.objects.bulk_create(objs, ignore_conflicts=True)
            print('imported successfully')
            returnmsg = {"status_code: 200"}
            success_url = reverse('events:list')
        except Exception as e:
            print('Error While Importing Data: ',e)
            returnmsg = {"status_code: 500"}
            success_url = reverse('events:list')
       
        return HttpResponse(returnmsg)
