from django.urls import path
from .views import (
    report_list_view,
    report_create_view,
    report_delete_view,
    report_detail_hx_view,
    report_detail_view,
    report_update_view,
    report_hx_mark_complete,
    report_hx_mark_pending
)

app_name='payroll'  # events:list

urlpatterns = [
    path("", report_list_view, name='list'),
    path("create/", report_create_view, name='create'),

    path("hx/<int:id>/", report_detail_hx_view, name='hx-detail'),
    path("hx/<int:id>/complete/", report_hx_mark_complete, name='hx-report-complete'),    
    path("hx/<int:id>/pending/", report_hx_mark_pending, name='hx-report-pending'),    
    path("<int:id>/delete/", report_delete_view, name='delete'),
    path("<int:id>/edit/", report_update_view, name='update'),
    path("<int:id>/", report_detail_view, name='detail'),

]