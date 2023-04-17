from django.urls import path

from . import views
app_name = 'main'

urlpatterns = [
    path('' , views.index , name='home'),
    path('news/' , views.news , name='news'),
    path('blog/' , views.blog , name='blog'),
    path('blog/search/' , views.blog_search , name='blog_search'),
    path('blog/<str:bl_str>/' , views.blog_single , name='blog_single'),
    path('news/<str:slug>/' , views.news_detal, name='news_detail'),
]
