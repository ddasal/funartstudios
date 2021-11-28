from django.urls import path
from .views import (
    SquareUpload,
    square_list_view
)

app_name='square'  # events:list

urlpatterns = [
    path("", square_list_view, name='list'),
    path('import/', SquareUpload.as_view(), name='import'),

]