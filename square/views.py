from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.http import HttpResponse,JsonResponse
from datetime import datetime
from django.urls.base import reverse
from django.views import View
from .models import Square
import io,csv
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

permission_required('square.view_square')
def square_list_view(request):
    qs = Square.objects.all().order_by('-date', '-time')
    page = request.GET.get('page', 1)

    paginator = Paginator(qs, 20)

    square_count = paginator.count
    try:
        square = paginator.page(page)
    except PageNotAnInteger:
        square = paginator.page(1)
    except EmptyPage:
        square = paginator.page(paginator.num_pages)

    context = {
        "square": square,
        "square_count": square_count,
    }
    return render(request, "square/list.html", context)

from datetime import datetime

# @permission_required('square.add_square')
class SquareUpload(LoginRequiredMixin, View):
    login_url = '/account/login/'

    def get(self, request):
        template_name = 'square/import-square.html'
        return render(request, template_name)

    def post(self, request):
        user = request.user #get the current login user details
        paramFile = io.TextIOWrapper(request.FILES['squarefile'].file)
        portfolio1 = csv.DictReader(paramFile)
        list_of_dict = list(portfolio1)
        objs = [
            Square(
                date=row['Date'],
                # date=datetime.strptime(row['Date'], '%M/%d/%y').strftime('%Y-%M-%d'), ## old method
                time=row['Time'],
                time_zone=row['Time Zone'],
                gross_sales=row['Gross Sales'].replace('$', ''),
                discounts=row['Discounts'].replace('$', ''),
                net_sales=row['Net Sales'].replace('$', ''),
                gift_card_sales=row['Gift Card Sales'].replace('$', ''),
                tax=row['Tax'].replace('$', ''),
                tip=row['Tip'].replace('$', ''),
                partial_refunds=row['Partial Refunds'].replace('$', ''),
                total_collected=row['Total Collected'].replace('$', ''),
                source=row['Source'],
                card=row['Card'].replace('$', ''),
                card_entry_methods=row['Card Entry Methods'],
                cash=row['Cash'].replace('$', ''),         
                square_gift_card=row['Square Gift Card'].replace('$', ''),      
                other_tender=row['Other Tender'].replace('$', ''),   
                other_tender_type=row['Other Tender Type'],           
                other_tender_note=row['Other Tender Note'],           
                fees=row['Fees'].replace('$', ''),
                net_total=row['Net Total'].replace('$', ''),        
                transaction_id=row['Transaction ID'],           
                payment_id=row['Payment ID'],           
                card_brand=row['Card Brand'],           
                pan_suffix=row['PAN Suffix'],           
                device_name=row['Device Name'],           
                staff_name=row['Staff Name'],           
                staff_id=row['Staff ID'],           
                details=row['Details'],           
                description=row['Description'],           
                event_type=row['Event Type'],           
                location=row['Location'],           
                customer_id=row['Customer ID'],           
                customer_name=row['Customer Name'],           
                customer_reference_id=row['Customer Reference ID'],           
                device_nickname=row['Device Nickname'],           
            )
            for row in list_of_dict
        ]
        try:
            msg = Square.objects.bulk_create(objs, ignore_conflicts=True)
            print('imported successfully')
            returnmsg = {"status_code": 200}
            success_url = reverse('square:list')
        except Exception as e:
            print('Error While Importing Data: ',e)
            returnmsg = {"status_code": 500}
            success_url = reverse('square:list')
       
        return redirect(success_url)
