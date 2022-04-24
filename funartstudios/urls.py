"""funartstudios URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from search.views import search_view

from .views import home_view, about_view, github_pull

urlpatterns = [
    path('', home_view, name='home'), # index / root / home
    path('githubpull/', github_pull, name='github'),
    path('about/', about_view), 
    path('account/', include('accounts.urls')),
    path('activities/', include('activities.urls')),
    path('articles/', include('articles.urls')),
    path('events/', include('events.urls')),
    path('payroll/', include('payroll.urls')),
    path('products/', include('products.urls')),
    path('royalty/', include('royaltyreports.urls')),
    path('schedule/', include('schedule.urls')),
    path('search/', search_view, name='search'),
    path('square/', include('square.urls')),
    path('taxes/', include('taxreports.urls')),
    path('util/', include('util.urls')),
    path('admin/', admin.site.urls),
]
