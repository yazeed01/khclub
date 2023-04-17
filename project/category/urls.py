from django.urls import path

from . import views

app_name = 'category'

urlpatterns = [
    path("programs/<str:slug>/" , views.data_category , name='data_category')
]
