from django.urls import path

from . import views

app_name = 'parts'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('download_datasheet/<int:part_id>/', views.download_datasheet,
         name='download_datasheet'),
    path('search/', views.search, name='search'),
    path('add_container/', views.add_container, name='add_container'),
]
