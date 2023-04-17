from django.urls import path
from . import views

app_name = 'competitions'

urlpatterns = [
    path('', views.CompetitionView.as_view(), name='competition'),
    path('ad_con_mana/', views.AdConManaView.as_view(), name='ad_con_mana'),
    path('<str:slug>/', views.quiz, name='quiz'),
    path('ad_con_mana_quiz/<int:qu_adm_id>/', views.ad_con_mana_quiz, name='ad_con_mana_quiz'),
]
