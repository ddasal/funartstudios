from django.urls import path
from .views import (
    event_list_view
    # event_detail_view,
    # event_create_view,
    # event_update_view,
    # event_detail_hx_view,
    # event_ingredient_update_hx_view,
    # event_delete_view,
    # event_ingredient_delete_view,
    # event_ingredient_image_upload_view
)

app_name='events'  # events:list

urlpatterns = [
    path("", event_list_view, name='list'),
    # path("create/", event_create_view, name='create'),

    # # path("hx/<int:parent_id>/ingredient/<int:id>", event_ingredient_update_hx_view, name='hx-ingredient-update'),
    # # path("hx/<int:parent_id>/ingredient/", event_ingredient_update_hx_view, name='hx-ingredient-create'),
    # path("hx/<int:id>/", event_detail_hx_view, name='hx-detail'),
    
    # # path("<int:parent_id>/image-upload/", event_ingredient_image_upload_view, name='event_ingredient_image_upload'),
    # # path("<int:parent_id>/ingredient/<int:id>/delete/", event_ingredient_delete_view, name='ingredient-delete'),
    # path("<int:id>/delete/", event_delete_view, name='delete'),
    # path("<int:id>/edit/", event_update_view, name='update'),
    # path("<slug:slug>/", event_detail_view, name='detail'),

]