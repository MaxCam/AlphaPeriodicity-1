"""periodicity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from calculatePeriodicity.views import PeriodicityAnalyzer,PeriodicityIndex
from django.views.generic.base import TemplateView
import calculatePeriodicity.views
import visualizePeriodicity.views

urlpatterns = [
    url(r'^periodicity/$', calculatePeriodicity.views.index, name='index'),
    url(r'^periodicity/calculate/$', PeriodicityAnalyzer.as_view()),
    url(r'^periodicity/visualize/$', visualizePeriodicity.views.visualize, name='visualize'),
]
