from django.urls import path
from .views import (
    schedule_list_view,
    schedule_staff_view,
    schedule_create_view,
    schedule_staff_edit_view,
    schedule_mgmt_review_view,
    schedule_mgmt_approve_view,
    schedule_staff_create_timeoff_view,
    schedule_staff_timeoff_detail_view,
    hx_schedule_staff_timeoff_detail_view,
    hx_schedule_mgmt_timeoff_detail_view,
    schedule_mgmt_timeoff_detail_view,
    schedule_staff_update_view,
    schedule_mgmt_approve_view,
    schedule_staff_timeoff_delete_view
)

app_name='schedule'  # events:list

urlpatterns = [
    path("", schedule_list_view, name='list'),
    path("create/", schedule_create_view, name='create'),
    path("staff/", schedule_staff_view, name='staff'),
    path("staff/approve/<int:id>", schedule_mgmt_approve_view, name='approve'),
    path("staff/edit", schedule_staff_edit_view, name='edit'),
    path("staff/review/<int:id>", schedule_mgmt_review_view, name='review'),
    path("staff/timeoff", schedule_staff_create_timeoff_view, name='timeoff'),
    path("staff/timeoff/<int:id>", schedule_staff_timeoff_detail_view, name='timeoffdetail'),
    path("mgmt/timeoff/<int:id>", schedule_mgmt_timeoff_detail_view, name='mgmttimeoffdetail'),
    path("staff/timeoff/hx/<int:id>", hx_schedule_staff_timeoff_detail_view, name='hx-timeoffdetail'),
    path("mgmt/timeoff/hx/<int:id>", hx_schedule_mgmt_timeoff_detail_view, name='hx-mgmttimeoffdetail'),

    path("staff/timeoff/<int:id>/update", schedule_staff_update_view, name='timeoffupdate'),
    path("mgmt/timeoff/<int:id>/approve", schedule_mgmt_approve_view, name='timeoffapprove'),
    path("staff/timeoff/<int:id>/delete", schedule_staff_timeoff_delete_view, name='timeoffdelete'),

]