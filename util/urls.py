from django.urls import path
from .views import (
    offsite_backup
)

app_name='util'

urlpatterns = [
    path("osb", offsite_backup, name='osb'),

]