from django.urls import path
from .views import (
    product_list_view,
    product_detail_view,
    product_create_view,
    product_update_view,
    product_detail_hx_view,
    product_delete_view,
    po_create_view,
    po_delete_view,
    po_detail_hx_view,
    po_detail_view,
    po_item_delete_view,
    po_item_update_hx_view,
    po_list_view,
    po_update_view
)

app_name='products'  # products:list

urlpatterns = [
    path("", product_list_view, name='list'),
    path("create/", product_create_view, name='create'),

    path("hx/<slug:slug>/", product_detail_hx_view, name='hx-detail'),
    
    # Purchases

    path("po/", po_list_view, name='po-list'),
    path("po/create/", po_create_view, name='po-create'),

    path("po/hx/<int:parent_id>/item/<int:id>", po_item_update_hx_view, name='hx-po-item-update'),
    path("po/hx/<int:parent_id>/item/", po_item_update_hx_view, name='hx-po-item-create'),
    path("po/hx/<int:id>/", po_detail_hx_view, name='hx-po-detail'),
    
    path("po/<int:parent_id>/staff/<int:id>/delete/", po_item_delete_view, name='po-item-delete'),
    path("po/<int:id>/delete/", po_delete_view, name='po-delete'),
    path("po/<int:id>/edit/", po_update_view, name='po-update'),
    path("po/<int:id>/", po_detail_view, name='po-detail'),


 # products again

    path("<slug:slug>/delete/", product_delete_view, name='delete'),
    path("<slug:slug>/edit/", product_update_view, name='update'),
    path("<slug:slug>/", product_detail_view, name='detail'),


]