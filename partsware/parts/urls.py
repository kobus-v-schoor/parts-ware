from django.urls import path

from . import views

app_name = 'parts'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('search/', views.search, name='search'),
]
