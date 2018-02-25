from django.urls import path, include

from . import views

app_name = 'gov'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'), # home
    path('desc', views.DescView.as_view(), name='desc'), # descending lease limit by 5
    path('asc', views.AscView.as_view(), name='asc'), # ascending lease limit by 5
    path('lease', views.LeaseDateView.as_view(), name='lease'), # get data between two dates
    path('add', views.DataCreate.as_view(), name='gov-add'), # add new data
    path('upload', views.upload_csv, name='upload_csv'), # upload csv
    path('count', views.CountView.as_view(), name='count'), # count number of mast by tenant
]