from django.urls import path
from .views import MainIdex, UploadPost

app_name = 'main'

urlpatterns = [
    path('', MainIdex.as_view(), name='index'),
    path('upload/', UploadPost.as_view(), name='upload')
]