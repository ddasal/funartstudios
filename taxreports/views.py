from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from events.models import Event, EventCustomer
from .forms import ReportForm
from django.db.models import Q, Sum
from taxreports.models import TaxReport
from square.models import Square
from decimal import Decimal
import io,csv
from django.views import View
from django.db.models.functions import TruncMonth
from itertools import groupby

# Create your views here.

@permission_required('taxreports.view_report')
def report_list_view(request):
    qs = TaxReport.objects.all().order_by('-start_date')
    page = request.GET.get('page', 1)

    paginator = Paginator(qs, 10)
    report_count = paginator.count
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    context = {
        "reports": reports,
        "report_count": report_count
    }
    return render(request, "taxreports/list.html", context)

@permission_required('taxreports.view_report')
def report_detail_view(request, id=None):
    hx_url = reverse("taxes:hx-detail", kwargs={"id": id})
    report_obj = TaxReport.objects.get(id=id)
    context = {
        "hx_url": hx_url,
        "report_obj": report_obj
    }
    return render(request, "taxreports/detail.html", context)


@permission_required('taxreports.delete_report')
def report_delete_view(request, id=None):
    try:
        obj = TaxReport.objects.get(id=id)
    except:
        obj = None
    if obj is None:
        if request.htmx:
            return HttpResponse('Not found')
        raise Http404
    if request.method == "POST":
        if obj.status == 'p':
            parent_obj = obj
            events = Event.objects.filter(tax_report=parent_obj)
            for each in events:
                each.tax_report = None
                each.save()
            obj.delete()
            success_url = reverse('taxes:list')
            if request.htmx:
                headers = {
                    "HX-Redirect": success_url
                }
                return HttpResponse('Success', headers=headers)
            return redirect(success_url)
        else:
            success_url = reverse('taxes:list')
            if request.htmx:
                headers = {
                    "HX-Redirect": success_url,
                }
                return HttpResponse('Success', headers=headers)
            return redirect(success_url)

    context = {
        "object": obj
    }
    return render(request, "taxreports/delete.html", context)


@permission_required('taxreports.view_report')
def report_detail_hx_view(request, id=None):
    if not request.htmx:
        raise Http404
    try:
        obj = TaxReport.objects.get(id=id)
        events = Event.objects.filter(date__range=(obj.start_date, obj.end_date)).order_by('date', 'time').prefetch_related()
        square_info = Square.objects.filter(date__range=(obj.start_date, obj.end_date)).exclude(taxable_sales=0).order_by('date')
        square_last_entry_date = Square.objects.latest('date', 'time')
        report_eventcustomer_cost_factors = Decimal(0.0)
        report_eventcustomer_taxes = Decimal(0.0)
        report_square_retail_sales = Decimal(0.0)
        report_squaresales_taxes = Decimal(0.0)
        report_total_taxable_sales = Decimal(0.0)
        report_total_taxes = Decimal(0.0)
        for each in events:
            each.temp_cost_factor = Decimal(0.0)
            temp_cost_factor = [Decimal(each.cost_factor) for each in EventCustomer.objects.filter(event=each.id).prefetch_related()]
            each.temp_cost_factor = sum(temp_cost_factor)
            report_eventcustomer_cost_factors = report_eventcustomer_cost_factors + each.temp_cost_factor

            each.temp_taxes = Decimal(0.0)
            temp_taxes = [Decimal(each.taxes) for each in EventCustomer.objects.filter(event=each.id)]
            each.temp_taxes = sum(temp_taxes)
            report_eventcustomer_taxes = report_eventcustomer_taxes + each.temp_taxes
        
        for sq in square_info:
            report_square_retail_sales = report_square_retail_sales + sq.taxable_sales
            report_squaresales_taxes = report_squaresales_taxes +sq.tax

        report_total_taxable_sales = Decimal(report_eventcustomer_cost_factors) + Decimal(report_square_retail_sales)
        report_total_taxes = Decimal(report_eventcustomer_taxes) + Decimal(report_squaresales_taxes)
        
        try:
            event_taxes = EventCustomer.objects.filter(date__range=(obj.start_date, obj.end_date)).order_by('date').prefetch_related()
            month_totals = {
                k: sum(x.taxes for x in g) 
                for k, g in groupby(event_taxes, key=lambda i: i.date.month)
            }
            # print(month_totals.keys())
            # print(month_totals.values())
            # mo_sales_tax = []
            # for month, total in month_totals.items():
            #     mo_sales_tax.append([month][total])
            # print(mo_sales_tax)
            # event_taxes_monthly = EventCustomer.objects.filter(event__date__range=(obj.start_date, obj.end_date)).order_by('event__date').prefetch_related().annotate(month=TruncMonth('event__date')).values('month').annotate(taxes=Sum(('taxes')))
        except Exception as e:
            print(e)

        # print(event_taxes_monthly)

        # for item in event_taxes_monthly:
        #     print(item)

        obj.eventcustomer_cost_factors = report_eventcustomer_cost_factors
        obj.eventcustomer_taxes = report_eventcustomer_taxes
        obj.square_retail_sales = report_square_retail_sales
        obj.squaresales_taxes = report_squaresales_taxes
        obj.total_taxable_sales = report_total_taxable_sales
        obj.total_taxes = report_total_taxes
        obj.save()
    except:
        obj = None
    if obj is None:
        return HttpResponse("Not found.")
    context = {
        "object": obj,
        "events": events,
        "square_last_entry_date": square_last_entry_date,
        "square": square_info,
        "report_eventcustomer_cost_factors": report_eventcustomer_cost_factors,
        "report_square_retail_sales": report_square_retail_sales,
        "month_totals": month_totals
    }
    return render(request, "taxreports/partials/detail.html", context)
 


@permission_required('royaltyreports.add_report')
def report_create_view(request):
    form = ReportForm(request.POST or None)
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
    return render(request, "taxreports/create-update.html", context) 

@permission_required('taxreports.change_report')
def report_update_view(request, id=None):
    obj = get_object_or_404(TaxReport, id=id)
    form = ReportForm(request.POST or None, instance=obj)
    context = {
        "form": form,
        "object": obj
    }
    if form.is_valid():
        form.save()
        context['message'] = 'Report data saved.'
    if request.htmx:
        return render(request, "taxreports/partials/forms.html", context)
    return render(request, "taxreports/create-update.html", context) 


@permission_required('taxreports.change_report')
def report_hx_mark_complete(request, id=None):
    # if not request.htmx:
    #     raise Http404
    try:
        parent_obj = TaxReport.objects.get(id=id)
    except:
        parent_obj = None

    if parent_obj is None:
        return HttpResponse("Not found.")
    else:
        parent_obj.status = 'c'
        parent_obj.save()
        children = Event.objects.filter(date__range=(parent_obj.start_date, parent_obj.end_date))
        other_children = Square.objects.filter(date__range=(parent_obj.start_date, parent_obj.end_date))
        for event in children:
            event.tax_report = parent_obj
            event.save()
        for square in other_children:
            square.status = 'c'
            square.save()
        success_url = reverse('taxes:list')
        return redirect(success_url)


@permission_required('taxreports.change_report')
def report_hx_mark_pending(request, id=None):
    try:
        parent_obj = TaxReport.objects.get(id=id)
    except:
        parent_obj = None

    if parent_obj is None:
        return HttpResponse("Not found.")
    else:
        children = Event.objects.filter(date__range=(parent_obj.start_date, parent_obj.end_date))
        for event in children:
            event.tax_report = None
            event.save()

        other_children = Square.objects.filter(date__range=(parent_obj.start_date, parent_obj.end_date))
        for square in other_children:
            square.status = 'p'
            square.save()

        parent_obj.status = 'p'
        parent_obj.save()
        success_url = reverse('taxes:list')
        return redirect(success_url)


class SquareUpload(View):
    def get(self, request):
        template_name = 'taxreports/import-square.html'
        return render(request, template_name)

    def post(self, request):
        user = request.user #get the current login user details
        paramFile = io.TextIOWrapper(request.FILES['squarefile'].file)
        portfolio1 = csv.DictReader(paramFile)
        list_of_dict = list(portfolio1)
        purgable_taxable_sales = Square.objects.filter(status='p')
        for item in purgable_taxable_sales:
            item.taxable_sales = Decimal(0.0)
            item.save()
            print('cleaned up old pending items before import')
        for row in list_of_dict:
            non_kit_taxable_sales = Decimal(0.0)
            square_row = Square.objects.get(transaction_id=row['Transaction ID'])
            if square_row.status == 'p':
                exclude_kits = 'Twist at Home Kit'
                exclude_events = 'Event'
                if exclude_kits not in row['Item'] and exclude_events not in row['Item']:
                    prev_taxable_sales_value = Decimal(square_row.taxable_sales)
                    square_row.taxable_sales = Decimal(prev_taxable_sales_value) + Decimal(row['Net Sales'].replace('$', ''),)
                    square_row.save()

        success_url = reverse('taxes:list')
        return redirect(success_url)
