
from django.urls import path

from .views import (
    faq_search_view,
    faq_create_view,
    faq_detail_view,
    faq_delete_view,
    faq_detail_hx_view,
    faq_update_view,
    faq_list_view,
)

app_name='faq' # faq:list 
urlpatterns = [
    path('', faq_list_view, name='list'),
    path('search/', faq_search_view, name='search'),
    path('create/', faq_create_view, name='create'),
    path('<slug:slug>/', faq_detail_view, name='detail'),
    path("<slug:slug>/edit/", faq_update_view, name='update'),
    path("<slug:slug>/delete/", faq_delete_view, name='delete'),
    path("hx/<slug:slug>/", faq_detail_hx_view, name='hx-detail'),

]
