from django.urls import path
from .views import MainIndex, UploadPost, PostLike

app_name = 'main'

urlpatterns = [
    path('', MainIndex.as_view(), name='index'),
    path('upload/', UploadPost.as_view(), name='upload'),
    path('cat/<int:pk>/', MainIndex.as_view(), name='cat'),
    path('post/<str:action>/<int:post_id>/', PostLike.as_view(), name='like')
]