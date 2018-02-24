from django.urls import path

from . import views

app_name = 'gov'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('add', views.DataCreate.as_view(), name='gov-add'),
]