from django.urls import path
from .views import MainIdex

app_name = 'main'

urlpatterns = [
    path('', MainIdex.as_view(), name='index')
]