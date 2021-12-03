from django.urls import path
from .views import (
    event_list_view,
    event_detail_view,
    event_create_view,
    event_update_view,
    event_detail_hx_view,
    event_staff_update_hx_view,
    event_delete_view,
    event_staff_delete_view,
    event_customer_delete_view,
    event_customer_update_hx_view,
    event_tip_update_hx_view,
    event_tip_delete_view,
    # EventCustomerUpload,
    # EventStaffUpload,
    event_search_view,
    event_image_update_hx_view,
    event_image_delete_view
)

app_name='events'  # events:list

urlpatterns = [
    path("", event_list_view, name='list'),
    path("search/", event_search_view, name='search'),
    path("create/", event_create_view, name='create'),
    # path('import/', EventCustomerUpload.as_view(), name='import'),

    path("hx/<slug:parent_slug>/customer/<int:id>", event_customer_update_hx_view, name='hx-eventcustomer-update'),
    path("hx/<slug:parent_slug>/customer/", event_customer_update_hx_view, name='hx-customer-create'),
    path("hx/<slug:parent_slug>/staff/<int:id>", event_staff_update_hx_view, name='hx-eventstaff-update'),
    path("hx/<slug:parent_slug>/staff/", event_staff_update_hx_view, name='hx-staff-create'),
    path("hx/<slug:parent_slug>/tip/<int:id>", event_tip_update_hx_view, name='hx-eventtip-update'),
    path("hx/<slug:parent_slug>/tip/", event_tip_update_hx_view, name='hx-tip-create'),
    path("hx/<slug:parent_slug>/image/<int:id>", event_image_update_hx_view, name='hx-eventimage-update'),
    path("hx/<slug:parent_slug>/image/", event_image_update_hx_view, name='hx-image-create'),
    path("hx/<slug:slug>/", event_detail_hx_view, name='hx-detail'),
    # path('importstaff/', EventStaffUpload.as_view(), name='importstaff'),
    
    # path("<slug:parent_slug>/image-upload/", event_image_upload_view, name='event-image-upload'),
    path("<slug:parent_slug>/customer/<int:id>/delete/", event_customer_delete_view, name='eventcustomer-delete'),
    path("<slug:parent_slug>/staff/<int:id>/delete/", event_staff_delete_view, name='eventstaff-delete'),
    path("<slug:parent_slug>/tip/<int:id>/delete/", event_tip_delete_view, name='eventtip-delete'),
    path("<slug:parent_slug>/image/<int:id>/delete/", event_image_delete_view, name='eventimage-delete'),
    path("<slug:slug>/delete/", event_delete_view, name='delete'),
    path("<slug:slug>/edit/", event_update_view, name='update'),
    path("<slug:slug>/", event_detail_view, name='detail'),

]