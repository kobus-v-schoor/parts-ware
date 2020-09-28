from django.urls import path

from . import views

app_name = 'parts'

urlpatterns = [
    path('index/', views.index, name='index'),
    path('download_datasheet/<int:part_id>/', views.download_datasheet,
         name='download_datasheet'),
    path('pinout/<int:part_id>/', views.pinout, name='pinout'),
    path('search/', views.search, name='search'),
    path('add_container/', views.add_container, name='add_container'),
    path('part/<int:part_id>/', views.view_part, name='view_part'),
    path('add_part/', views.add_part, name='add_part'),
    path('edit_part/<int:part_id>/', views.edit_part, name='edit_part'),
    path('delete_part/<int:part_id>/', views.delete_part, name='delete_part'),
]
