from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.http import HttpResponse, JsonResponse
from django.http.response import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q, Sum
from .forms import ActivityAdminPayForm, ActivityForm, ActivityImageForm, ActivityStaffForm, ActivityCustomerForm, ActivityTipForm
from .models import ActivityAdminPay, Activity, ActivityCustomer, ActivityImages, ActivityStaff, ActivityTip
from royaltyreports.models import RoyaltyReport
from datetime import datetime, timedelta
from django.views import View
import io,csv
from decimal import Decimal


# Create your views here.

@permission_required('payroll.view_report')
def activity_list_view(request):
    N_DAYS_AGO = 30
    N_DAYS_FUTURE = 2
    today = datetime.now()    
    n_days_ago = today - timedelta(days=N_DAYS_AGO)
    n_days_future = today + timedelta(days=N_DAYS_FUTURE)
    date_min = n_days_ago.strftime("%Y-%m-%d") # '2020-03-31'
    date_max = n_days_future.strftime("%Y-%m-%d")
    query = ''
    qs = Activity.objects.filter(active=True, date__range=[date_min, date_max]).order_by('-date', '-time')
    page = request.GET.get('page', 1)

    paginator = Paginator(qs, 10)

    activity_count = paginator.count
    try:
        activities = paginator.page(page)
    except PageNotAnInteger:
        activities = paginator.page(1)
    except EmptyPage:
        activities = paginator.page(paginator.num_pages)

    context = {
        "activities": activities,
        "activity_count": activity_count,
        "date_min": date_min,
        "date_max": date_max,
        "q": query
    }
    return render(request, "activities/list.html", context)


@permission_required('activities.view_activity')
def activity_search_view(request):
    query = request.GET.get('q')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    lookups = Q(title__icontains=query) | Q(activitystaff__user__first_name__icontains=query)  | Q(activitystaff__user__last_name__icontains=query) | Q(activitystaff__prepaint_product__name__icontains=query) | Q(activitystaff__activity_product__name__icontains=query) | Q(activitycustomer__product__name__icontains=query)
    qs = Activity.objects.filter(lookups, date__range=[date_min, date_max]).order_by('-date', '-time').distinct()
    page = request.GET.get('page', 1)

    paginator = Paginator(qs, 10)

    activity_count = paginator.count
    try:
        activities = paginator.page(page)
    except PageNotAnInteger:
        activities = paginator.page(1)
    except EmptyPage:
        activities = paginator.page(paginator.num_pages)

    context = {
        "activities": activities,
        "activity_count": activity_count,
        "date_min": date_min,
        "date_max": date_max,
        "q": query
    }
    return render(request, "activities/search.html", context)

@permission_required('activities.view_activity')
def activity_detail_view(request, slug=None):
    hx_url = reverse("activities:hx-detail", kwargs={"slug": slug})
    activity_obj = Activity.objects.get(slug=slug)
    context = {
        "hx_url": hx_url,
        "activity_obj": activity_obj
    }
    return render(request, "activities/detail.html", context)






@permission_required('activities.delete_activity')
def activity_delete_view(request, slug=None):
    try:
        obj = Activity.objects.get(slug=slug)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse('Not found')
        raise Http404
    if request.method == "POST":
        if obj.status == 'p':
            obj.delete()
            success_url = reverse('activities:list')
            if request.htmx:
                headers = {
                    "HX-Redirect": success_url
                }
                return HttpResponse('Success', headers=headers)
            return redirect(success_url)
        else:
            success_url = reverse('activities:list')
            if request.htmx:
                headers = {
                    "HX-Redirect": success_url,
                }
                return HttpResponse('Success', headers=headers)
            return redirect(success_url)

    context = {
        "object": obj
    }
    return render(request, "activities/delete.html", context)

@permission_required('activities.delete_activitystaff')
def activity_staff_delete_view(request, parent_slug=None, id=None):
    try:
        obj = ActivityStaff.objects.get(activity__slug=parent_slug, id=id)
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
            success_url = reverse('activities:detail', kwargs={"slug": parent_slug})
            if request.htmx:
                return render(request, "activities/partials/staff-inline-delete-response.html", {"staff": staff})
            return redirect(success_url)
        else:
            message = "Unable to delete."
            success_url = reverse('activities:detail', kwargs={"slug": parent_slug})
            if request.htmx:
                return render(request, "activities/partials/staff-inline-delete-response.html", {"message": message})
            return redirect(success_url)

    context = {
        "object": obj
    }
    return render(request, "activities/delete.html", context)


@permission_required('activities.delete_activitycustomer')
def activity_customer_delete_view(request, parent_slug=None, id=None):
    try:
        obj = ActivityCustomer.objects.get(activity__slug=parent_slug, id=id)
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
            success_url = reverse('activities:detail', kwargs={"slug": parent_slug})
            if request.htmx:
                return render(request, "activities/partials/customer-inline-delete-response.html", {"customer": customer})
            return redirect(success_url)
        else:
            message = "Unable to delete."
            success_url = reverse('activities:detail', kwargs={"slug": parent_slug})
            if request.htmx:
                return render(request, "activities/partials/customer-inline-delete-response.html", {"message": message})
            return redirect(success_url)
    context = {
        "object": obj
    }
    return render(request, "activities/delete.html", context)



@permission_required('activities.view_activity')
def activity_detail_hx_view(request, slug=None):
    if not request.htmx:
        raise Http404
    try:
        obj = Activity.objects.get(slug=slug)
        try:
            revenue = ActivityCustomer.objects.filter(activity_id=obj.id).aggregate(Sum('total_price'))
            if revenue['total_price__sum'] is None:
                revenue['total_price__sum'] = Decimal(0.0)
                royalty_fees = Decimal(0.0)
            else:
                royalty_fees = Decimal(revenue['total_price__sum']) * Decimal(0.08)
            taxes = ActivityCustomer.objects.filter(activity_id=obj.id).aggregate(Sum('taxes'))
            if taxes['taxes__sum'] is None:
                taxes['taxes__sum'] = Decimal(0.0)
            labor = ActivityStaff.objects.filter(activity_id=obj.id).aggregate(Sum('total_pay'))
            if labor['total_pay__sum'] is None:
                labor['total_pay__sum'] = Decimal(0.0)
                loaded_labor = Decimal(0.0)
            else:
                loaded_labor = Decimal(labor['total_pay__sum']) * Decimal(1.075)
            customer_product_costs_only = ActivityCustomer.objects.filter(activity_id=obj.id).aggregate(Sum('product_cost')) 
            if customer_product_costs_only['product_cost__sum'] is None:
                customer_product_costs_only['product_cost__sum'] = Decimal(0.0)
            customer_product_costs = ActivityCustomer.objects.filter(activity_id=obj.id).aggregate(Sum('cost_factor')) 
            if customer_product_costs['cost_factor__sum'] is None:
                customer_product_costs['cost_factor__sum'] = Decimal(0.0)
            staff_product_costs = ActivityStaff.objects.filter(activity_id=obj.id).aggregate(Sum('cost_factor'))
            if staff_product_costs['cost_factor__sum'] is None:
                staff_product_costs['cost_factor__sum'] = Decimal(0.0)
            
            gp = Decimal(revenue['total_price__sum']) - Decimal(loaded_labor) - Decimal(customer_product_costs_only['product_cost__sum']) - Decimal(staff_product_costs['cost_factor__sum']) - Decimal(royalty_fees) - Decimal(taxes['taxes__sum'])
            formatted_gp = round(gp, 2)
        except Exception as e:
            print(e)
            formatted_gp = Decimal(0.0)
        new_staff_url = reverse("activities:hx-staff-create", kwargs={"parent_slug": obj.slug})
        new_customer_url = reverse("activities:hx-customer-create", kwargs={"parent_slug": obj.slug})
        new_tip_url = reverse("activities:hx-tip-create", kwargs={"parent_slug": obj.slug})
        new_image_url = reverse("activities:hx-image-create", kwargs={"parent_slug": obj.slug})
        new_activityadminpay_url = reverse("activities:hx-activityadminpay-create", kwargs={"parent_slug": obj.slug})
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
        "new_activityadminpay_url": new_activityadminpay_url,
        "gp": formatted_gp
    }
    return render(request, "activities/partials/detail.html", context)
 


@permission_required('activities.add_activity')
def activity_create_view(request):
    form = ActivityForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        royalty_date_check = RoyaltyReport.objects.filter(end_date__gte=obj.date, start_date__lte=obj.date, status='c')
        if royalty_date_check:
            return HttpResponse("Unable to create activity. Check that your date isn't conflicting with a closed Pay Period or Royalty Report.")
        else:
            obj.created_by = request.user
            obj.user = request.user
            obj.save()
            if request.htmx:
                headers = {
                    "HX-Redirect": obj.get_absolute_url()
                }
                return HttpResponse('Created', headers=headers)
            return redirect(obj.get_absolute_url())
    return render(request, "activities/create-update.html", context) 

@permission_required('activities.change_activity')
def activity_update_view(request, slug=None):
    obj = get_object_or_404(Activity, slug=slug)
    form = ActivityForm(request.POST or None, instance=obj)
    new_staff_url = reverse("activities:hx-staff-create", kwargs={"parent_slug": obj.slug})
    new_customer_url = reverse("activities:hx-customer-create", kwargs={"parent_slug": obj.slug})
    new_tip_url = reverse("activities:hx-tip-create", kwargs={"parent_slug": obj.slug})
    new_image_url = reverse("activities:hx-image-create", kwargs={"parent_slug": obj.slug})
    new_activityadminpay_url = reverse("activities:hx-activityadminpay-create", kwargs={"parent_slug": obj.slug})
    context = {
        "form": form,
        "object": obj,
        "new_staff_url": new_staff_url,
        "new_customer_url": new_customer_url,
        "new_tip_url": new_tip_url,
        "new_activityadminpay_url": new_activityadminpay_url,
        "new_image_url": new_image_url
    }
    if form.is_valid():
        obj.updated_by = request.user
        obj.save()
        form.save()
        context['message'] = 'Activity data saved.'
    if request.htmx:
        return render(request, "activities/partials/forms.html", context)
    return render(request, "activities/create-update.html", context) 


@permission_required('activities.change_activitystaff')
def activity_staff_update_hx_view(request, parent_slug=None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_obj = Activity.objects.get(slug=parent_slug)
    except:
        parent_obj = None
    if parent_obj is None:
        return HttpResponse("Not found.")

    instance = None
    if id is not None:
        try:
            instance = ActivityStaff.objects.get(activity=parent_obj, id=id)
        except:
            instance = None
    form = ActivityStaffForm(request.POST or None, instance=instance)
    url = reverse("activities:hx-staff-create", kwargs={"parent_slug": parent_obj.slug})
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
            new_obj.activity = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, "activities/partials/staff-inline.html", context)
    
    return render(request, "activities/partials/staff-form.html", context)




@permission_required('activities.change_activitycustomer')
def activity_customer_update_hx_view(request, parent_slug=None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_obj = Activity.objects.get(slug=parent_slug)
    except:
        parent_obj = None
    if parent_obj is None:
        return HttpResponse("Not found.")

    instance = None
    if id is not None:
        try:
            instance = ActivityCustomer.objects.get(activity=parent_obj, id=id)
        except:
            instance = None
    form = ActivityCustomerForm(request.POST or None, instance=instance)
    url = reverse("activities:hx-customer-create", kwargs={"parent_slug": parent_obj.slug})
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
            new_obj.activity = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, "activities/partials/customer-inline.html", context)
    
    return render(request, "activities/partials/customer-form.html", context)



@permission_required('activities.change_activitytip')
def activity_tip_update_hx_view(request, parent_slug=None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_obj = Activity.objects.get(slug=parent_slug)
    except:
        parent_obj = None
    if parent_obj is None:
        return HttpResponse("Not found.")

    instance = None
    if id is not None:
        try:
            instance = ActivityTip.objects.get(activity=parent_obj, id=id)
        except:
            instance = None
    form = ActivityTipForm(request.POST or None, instance=instance)
    url = reverse("activities:hx-tip-create", kwargs={"parent_slug": parent_obj.slug})
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
            new_obj.activity = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, "activities/partials/tip-inline.html", context)
    
    return render(request, "activities/partials/tip-form.html", context)

@permission_required('activities.delete_activitytip')
def activity_tip_delete_view(request, parent_slug=None, id=None):
    try:
        obj = ActivityTip.objects.get(activity__slug=parent_slug, id=id)
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
            success_url = reverse('activities:detail', kwargs={"slug": parent_slug})
            if request.htmx:
                return render(request, "activities/partials/tip-inline-delete-response.html", {"tip": tip})
            return redirect(success_url)
        else:
            message = "Unable to delete."
            success_url = reverse('activities:detail', kwargs={"slug": parent_slug})
            if request.htmx:
                return render(request, "activities/partials/tip-inline-delete-response.html", {"message": message})
            return redirect(success_url)

    context = {
        "object": obj
    }
    return render(request, "activities/delete.html", context)




# @login_required
class ActivityStaffUpload(View):
    def get(self, request):
        template_name = 'activities/import-staff.html'
        return render(request, template_name)
    def post(self, request):
        user = request.user #get the current login user details
        paramFile = io.TextIOWrapper(request.FILES['activitystaff'].file)
        portfolio1 = csv.DictReader(paramFile)
        list_of_dict = list(portfolio1)
        objs = [
            ActivityStaff(
            role=row['role'],
            hours=row['hours'],
            activity_id=row['activity_id'],
            user_id=row['new_user_id'],
            # activity_qty=row['activity_qty'],
            # prepaint_qty=row['prepaint_qty'],
            # activity_product_id=row['activity_product'],
            # prepaint_product_id=row['prepaint_product'],
         )
         for row in list_of_dict
     ]
        try:
            msg = ActivityStaff.objects.bulk_create(objs)
            returnmsg = {"status_code": 200}
            print('imported successfully')
        except Exception as e:
            print('Error While Importing Data: ',e)
            returnmsg = {"status_code": 500}
       
        return JsonResponse(returnmsg)


from decimal import Decimal

# @permission_required('square.add_square')
class ActivityCustomerUpload(View):
    def get(self, request):
        template_name = 'activities/import-activitycustomers.html'
        return render(request, template_name)

    def post(self, request):
        user = request.user #get the current login user details
        paramFile = io.TextIOWrapper(request.FILES['activityfile'].file)
        portfolio1 = csv.DictReader(paramFile)
        list_of_dict = list(portfolio1)
        objs = [
            ActivityCustomer(
                type='r',
                quantity=row['surface_qty'],
                activity_id=row['activity_id'],
                per_customer_qty='1',
                product_id=row['surface_id'],
                price=row['surface_price'],
                status='c',
            )
            for row in list_of_dict
        ]
        try:
            msg = ActivityCustomer.objects.bulk_create(objs, ignore_conflicts=True)
            print('imported successfully')
            returnmsg = {"status_code: 200"}
            success_url = reverse('activities:list')
        except Exception as e:
            print('Error While Importing Data: ',e)
            returnmsg = {"status_code: 500"}
            success_url = reverse('activities:list')
       
        return HttpResponse(returnmsg)



@permission_required('activities.change_activityimages')
def activity_image_update_hx_view(request, parent_slug=None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_obj = Activity.objects.get(slug=parent_slug)
    except:
        parent_obj = None
    if parent_obj is None:
        return HttpResponse("Not found.")

    instance = None
    if id is not None:
        try:
            instance = ActivityImages.objects.get(activity=parent_obj, id=id)
        except:
            instance = None
    form = ActivityImageForm(request.POST or None, request.FILES or None, instance=instance)
    url = reverse("activities:hx-image-create", kwargs={"parent_slug": parent_obj.slug})
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
            new_obj.activity = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, "activities/partials/image-inline.html", context)
    
    return render(request, "activities/partials/image-form.html", context)



@permission_required('activities.delete_activityimages')
def activity_image_delete_view(request, parent_slug=None, id=None):
    try:
        obj = ActivityImages.objects.get(activity__slug=parent_slug, id=id)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse('Not found')
        raise Http404
    if request.method == "POST":
        title = obj.title
        obj.delete()
        success_url = reverse('activities:detail', kwargs={"slug": parent_slug})
        if request.htmx:
            return render(request, "activities/partials/image-inline-delete-response.html", {"title": title})
        return redirect(success_url)

    context = {
        "object": obj
    }
    return render(request, "activities/delete.html", context)





@permission_required('activities.change_activityadminpay')
def activityadmin_pay_update_hx_view(request, parent_slug=None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_obj = Activity.objects.get(slug=parent_slug)
    except:
        parent_obj = None
    if parent_obj is None:
        return HttpResponse("Not found.")

    instance = None
    if id is not None:
        try:
            instance = ActivityAdminPay.objects.get(activity=parent_obj, id=id)
        except:
            instance = None
    form = ActivityAdminPayForm(request.POST or None, instance=instance)
    url = reverse("activities:hx-activityadminpay-create", kwargs={"parent_slug": parent_obj.slug})
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
            new_obj.activity = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, "activities/partials/activityadminpay-inline.html", context)
    
    return render(request, "activities/partials/activityadminpay-form.html", context)

@permission_required('activities.delete_activityadminpay')
def activityadmin_pay_delete_view(request, parent_slug=None, id=None):
    try:
        obj = ActivityAdminPay.objects.get(activity__slug=parent_slug, id=id)
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
            success_url = reverse('activities:detail', kwargs={"slug": parent_slug})
            if request.htmx:
                return render(request, "activities/partials/activityadminpay-inline-delete-response.html", {"staff": staff})
            return redirect(success_url)
        else:
            message = "Unable to delete."
            success_url = reverse('activities:detail', kwargs={"slug": parent_slug})
            if request.htmx:
                return render(request, "activities/partials/activityadminpay-inline-delete-response.html", {"message": message})
            return redirect(success_url)

    context = {
        "object": obj
    }
    return render(request, "activities/delete.html", context)


@login_required
def report_staff_list_view(request):
    N_DAYS_AGO = 30
    N_DAYS_FUTURE = 2
    today = datetime.now()    
    n_days_ago = today - timedelta(days=N_DAYS_AGO)
    n_days_future = today + timedelta(days=N_DAYS_FUTURE)
    date_min = n_days_ago.strftime("%Y-%m-%d") # '2020-03-31'
    date_max = n_days_future.strftime("%Y-%m-%d")
    query = ''
    qs = Activity.objects.filter(active=True, date__range=[date_min, date_max], activitystaff__user=request.user.id).order_by('-date', '-time')
    page = request.GET.get('page', 1)

    paginator = Paginator(qs, 10)

    activity_count = paginator.count
    try:
        activities = paginator.page(page)
    except PageNotAnInteger:
        activities = paginator.page(1)
    except EmptyPage:
        activities = paginator.page(paginator.num_pages)

    context = {
        "activities": activities,
        "activity_count": activity_count,
        "date_min": date_min,
        "date_max": date_max,
        "q": query
    }

    return render(request, "activities/staff-list.html", context)

