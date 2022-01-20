from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from aggregator import views

app_name = 'aggregator'

router = DefaultRouter()
router.register('', views.EventView)

urlpatterns = [
    path('crud/', include(router.urls)),
    path("counter/", views.CounterView.as_view(), name="counter"),
    path("statistics/", views.StatisticsView.as_view(), name="statistics"),
]