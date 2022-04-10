from django.urls import path
from .views import (
    schedule_list_view,
    schedule__staff_view,
    schedule_create_view
)

app_name='schedule'  # events:list

urlpatterns = [
    path("", schedule_list_view, name='list'),
    path("create/", schedule_create_view, name='create'),
    path("staff/", schedule__staff_view, name='staff'),

]