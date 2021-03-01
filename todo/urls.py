from todowebsite.todo import views
from django.urls import path


urlPatterns = [
    path('/apis',views.apiOverview,name='api-overview')
]