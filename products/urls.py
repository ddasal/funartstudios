from django.urls import path
from .views import (
    product_list_view,
    product_detail_view,
    product_create_view,
    product_update_view,
    product_detail_hx_view,
    product_delete_view
)

app_name='products'  # products:list

urlpatterns = [
    path("", product_list_view, name='list'),
    path("create/", product_create_view, name='create'),

    path("hx/<slug:slug>/", product_detail_hx_view, name='hx-detail'),
    
    path("<slug:slug>/delete/", product_delete_view, name='delete'),
    path("<slug:slug>/edit/", product_update_view, name='update'),
    path("<slug:slug>/", product_detail_view, name='detail'),

]