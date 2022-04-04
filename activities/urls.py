from django.urls import path
from .views import (
    activity_list_view,
    activity_detail_view,
    activity_create_view,
    activity_update_view,
    activity_detail_hx_view,
    activity_staff_update_hx_view,
    activity_delete_view,
    activity_staff_delete_view,
    activity_customer_delete_view,
    activity_customer_update_hx_view,
    activity_tip_update_hx_view,
    activity_tip_delete_view,
    activity_search_view,
    activity_image_update_hx_view,
    activity_image_delete_view,
    activityadmin_pay_delete_view,
    activityadmin_pay_update_hx_view,
    report_staff_list_view
)

app_name='activities'  

urlpatterns = [
    path("", activity_list_view, name='list'),
    path("staff/", report_staff_list_view, name='staff-list'),
    path("search/", activity_search_view, name='search'),
    path("create/", activity_create_view, name='create'),

    path("hx/<slug:parent_slug>/customer/<int:id>", activity_customer_update_hx_view, name='hx-activitycustomer-update'),
    path("hx/<slug:parent_slug>/customer/", activity_customer_update_hx_view, name='hx-customer-create'),
    path("hx/<slug:parent_slug>/staff/<int:id>", activity_staff_update_hx_view, name='hx-activitystaff-update'),
    path("hx/<slug:parent_slug>/staff/", activity_staff_update_hx_view, name='hx-staff-create'),
    path("hx/<slug:parent_slug>/tip/<int:id>", activity_tip_update_hx_view, name='hx-activitytip-update'),
    path("hx/<slug:parent_slug>/tip/", activity_tip_update_hx_view, name='hx-tip-create'),
    path("hx/<slug:parent_slug>/image/<int:id>", activity_image_update_hx_view, name='hx-activityimage-update'),
    path("hx/<slug:parent_slug>/image/", activity_image_update_hx_view, name='hx-image-create'),
    path("hx/<slug:slug>/", activity_detail_hx_view, name='hx-detail'),
    path("hx/<slug:parent_slug>/adminpay/<int:id>", activityadmin_pay_update_hx_view, name='hx-activityadminpay-update'),
    path("hx/<slug:parent_slug>/adminpay/", activityadmin_pay_update_hx_view, name='hx-activityadminpay-create'),

    path("<slug:parent_slug>/customer/<int:id>/delete/", activity_customer_delete_view, name='activitycustomer-delete'),
    path("<slug:parent_slug>/staff/<int:id>/delete/", activity_staff_delete_view, name='activitystaff-delete'),
    path("<slug:parent_slug>/tip/<int:id>/delete/", activity_tip_delete_view, name='activitytip-delete'),
    path("<slug:parent_slug>/image/<int:id>/delete/", activity_image_delete_view, name='activityimage-delete'),
    path("<slug:slug>/delete/", activity_delete_view, name='delete'),
    path("<slug:slug>/edit/", activity_update_view, name='update'),
    path("<slug:slug>/", activity_detail_view, name='detail'),
    path("<slug:parent_slug>/adminpay/<int:id>/delete/", activityadmin_pay_delete_view, name='activityadminpay-delete'),

]