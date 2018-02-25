from django.urls import path

from . import views

app_name = 'gov'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('desc', views.DescView.as_view(), name='desc'),
    path('asc', views.AscView.as_view(), name='asc'),
    path('add', views.DataCreate.as_view(), name='gov-add'),
    path('upload', views.upload_csv, name='upload_csv'),
]