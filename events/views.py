from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.http import HttpResponse, JsonResponse
from django.http.response import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q, Sum
from .forms import EventForm, EventImageForm, EventStaffForm, EventCustomerForm, EventTipForm
from .models import Event, EventCustomer, EventImages, EventStaff, EventTip
from royaltyreports.models import RoyaltyReport
from datetime import datetime, timedelta
from django.views import View
import io,csv
from decimal import Decimal


# Create your views here.

@permission_required('events.view_event')
def event_list_view(request):
    N_DAYS_AGO = 10
    N_DAYS_FUTURE = 5
    today = datetime.now()    
    n_days_ago = today - timedelta(days=N_DAYS_AGO)
    n_days_future = today + timedelta(days=N_DAYS_FUTURE)
    date_min = '2020-03-31' #n_days_ago.strftime("%Y-%m-%d")
    date_max = n_days_future.strftime("%Y-%m-%d")
    query = ''
    qs = Event.objects.filter(active=True, date__range=[date_min, date_max]).order_by('-date', '-time')
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
        "date_min": date_min,
        "date_max": date_max,
        "q": query
    }
    return render(request, "events/list.html", context)


@permission_required('events.view_event')
def event_search_view(request):
    query = request.GET.get('q')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    lookups = Q(title__icontains=query) | Q(eventstaff__user__first_name__icontains=query)  | Q(eventstaff__user__last_name__icontains=query) | Q(eventstaff__prepaint_product__name__icontains=query) | Q(eventstaff__event_product__name__icontains=query) | Q(eventcustomer__product__name__icontains=query)
    qs = Event.objects.filter(lookups, date__range=[date_min, date_max]).order_by('-date', '-time').distinct()
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
        "date_min": date_min,
        "date_max": date_max,
        "q": query
    }
    return render(request, "events/search.html", context)

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
        # revenue = EventCustomer.objects.filter(event_id=obj.id).aggregate(Sum('total_price'))
        # taxes = EventCustomer.objects.filter(event_id=obj.id).aggregate(Sum('taxes'))
        # labor = EventStaff.objects.filter(event_id=obj.id).aggregate(Sum('total_pay'))
        # customer_product_costs = EventCustomer.objects.filter(event_id=obj.id).aggregate(Sum('cost_factor'))
        # staff_product_costs = EventStaff.objects.filter(event_id=obj.id).aggregate(Sum('cost_factor'))
        # royalty_fees = Decimal(revenue['total_price__sum']) * Decimal(0.08)
        # loaded_labor = Decimal(labor['total_pay__sum']) * Decimal(1.075)
        # gp = Decimal(revenue['total_price__sum']) - Decimal(loaded_labor) - Decimal(customer_product_costs['cost_factor__sum']) - Decimal(staff_product_costs['cost_factor__sum']) - Decimal(royalty_fees) - Decimal(taxes['taxes__sum'])
        # formatted_gp = round(gp, 2)
        new_staff_url = reverse("events:hx-staff-create", kwargs={"parent_slug": obj.slug})
        new_customer_url = reverse("events:hx-customer-create", kwargs={"parent_slug": obj.slug})
        new_tip_url = reverse("events:hx-tip-create", kwargs={"parent_slug": obj.slug})
        new_image_url = reverse("events:hx-image-create", kwargs={"parent_slug": obj.slug})
    except:
        obj = None
    if obj is None:
        return HttpResponse("Not found.")
    context = {
        "object": obj,
        "new_staff_url": new_staff_url,
        "new_customer_url": new_customer_url,
        "new_tip_url": new_tip_url,
        "new_image_url": new_image_url,
        # "gp": formatted_gp
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
            obj.created_by = request.user
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
    new_image_url = reverse("events:hx-image-create", kwargs={"parent_slug": obj.slug})
    context = {
        "form": form,
        "object": obj,
        "new_staff_url": new_staff_url,
        "new_customer_url": new_customer_url,
        "new_tip_url": new_tip_url,
        "new_image_url": new_image_url
    }
    if form.is_valid():
        obj.updated_by = request.user
        obj.save()
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
            # event_qty=row['event_qty'],
            # prepaint_qty=row['prepaint_qty'],
            # event_product_id=row['event_product'],
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



@permission_required('events.change_eventimages')
def event_image_update_hx_view(request, parent_slug=None, id=None):
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
            instance = EventImages.objects.get(event=parent_obj, id=id)
        except:
            instance = None
    form = EventImageForm(request.POST or None, request.FILES or None, instance=instance)
    url = reverse("events:hx-image-create", kwargs={"parent_slug": parent_obj.slug})
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
        return render(request, "events/partials/image-inline.html", context)
    
    return render(request, "events/partials/image-form.html", context)




# @permission_required('events.add_eventimage')
# def event_image_update_hx_view(request, parent_slug=None):
#     template_name = "events/upload-image.html"
#     if request.htmx:
#         template_name = "events/partials/image-form.html"
#     try:
#         parent_obj = Event.objects.get(slug=parent_slug)
#     except:
#         parent_obj = None
#     if parent_obj is None:
#         raise Http404
#     form = EventImageForm(request.POST or None, request.FILES or None)
#     if form.is_valid():
#         obj = form.save(commit=False)
#         obj.event = parent_obj
#         obj.save()
#         success_url = parent_obj.get_absolute_url()
#         if request.htmx:
#             headers = {
#                 'HX-Redirect': success_url
#             }
#             return HttpResponse("Success", headers=headers)
#         return redirect(success_url)

#     return render(request, template_name, {"form":form})

@permission_required('events.delete_eventimages')
def event_image_delete_view(request, parent_slug=None, id=None):
    try:
        obj = EventImages.objects.get(event__slug=parent_slug, id=id)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse('Not found')
        raise Http404
    if request.method == "POST":
        title = obj.title
        obj.delete()
        success_url = reverse('events:detail', kwargs={"slug": parent_slug})
        if request.htmx:
            return render(request, "events/partials/image-inline-delete-response.html", {"title": title})
        return redirect(success_url)

    context = {
        "object": obj
    }
    return render(request, "events/delete.html", context)


