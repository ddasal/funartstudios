from django.urls import path
from .views import (
    schedule_list_view,
    schedule_staff_view,
    schedule_create_view,
    schedule_staff_edit_view,
    schedule_mgmt_review_view,
    schedule_mgmt_approve_view
)

app_name='schedule'  # events:list

urlpatterns = [
    path("", schedule_list_view, name='list'),
    path("create/", schedule_create_view, name='create'),
    path("staff/", schedule_staff_view, name='staff'),
    path("staff/approve/<int:id>", schedule_mgmt_approve_view, name='approve'),
    path("staff/edit", schedule_staff_edit_view, name='edit'),
    path("staff/review/<int:id>", schedule_mgmt_review_view, name='review'),

]