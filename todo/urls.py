from . import views
from django.urls import path


urlPatterns = [
    path('',views.apiOverview,name='api-overview')
]