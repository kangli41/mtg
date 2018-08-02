"""riverrun URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^card_update$', views.card_update, name='card_update'),
    url(r'^history/$', views.trade_history, name='trade_history'),
    url(r'^scrubber$', views.card_scrubber, name='card_scrubber'),
    url(r'^card_sell/(.*)$', views.card_sell, name='card_sell'),
    url(r'^card_analysis$', views.card_analysis, name='card_analysis'),
    
    # url(r'^detail/(.+)$', views.league_detail, name='league_detail'),
    # url(r'^history/$', views.battle_history, name='battle_history'),
    # url(r'^history/(.+)$', views.battle_history_detail, name='battle_history_detail'),
]
