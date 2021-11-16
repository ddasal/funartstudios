
from django.urls import path

from .views import (
    article_search_view,
    article_create_view,
    article_detail_view,
    article_delete_view,
    article_detail_hx_view,
    article_update_view,
    article_comment_update_hx_view,
    article_comment_delete_view
)

app_name='articles' # articles:list 
urlpatterns = [
    path('', article_search_view, name='search'),
    path('create/', article_create_view, name='create'),
    path('<slug:slug>/', article_detail_view, name='detail'),
    path("<slug:slug>/edit/", article_update_view, name='update'),
    path("<slug:slug>/delete/", article_delete_view, name='delete'),
    path("hx/<slug:slug>/", article_detail_hx_view, name='hx-detail'),

    path("hx/<slug:parent_slug>/comment/<int:id>", article_comment_update_hx_view, name='hx-comment-update'),
    path("hx/<slug:parent_slug>/comment/", article_comment_update_hx_view, name='hx-comment-create'),
    path("<slug:parent_slug>/comment/<int:id>/delete/", article_comment_delete_view, name='comment-delete'),

]
