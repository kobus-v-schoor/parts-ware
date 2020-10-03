from django.urls import path

from . import views

app_name = 'parts'

urlpatterns = [
    path('', views.index, name='index'),
    path('media/<str:media_type>/<int:part_id>/', views.media, name='media'),
    path('search/', views.search, name='search'),
    path('all_parts/', views.all_parts, name='all_parts'),
    path('list_containers/', views.list_containers, name='list_containers'),
    path('add_container/', views.add_container, name='add_container'),
    path('edit_container/<int:container_id>/', views.edit_container,
         name='edit_container'),
    path('delete_container/<int:container_id>/', views.delete_container,
         name='delete_container'),
    path('part/<int:part_id>/', views.view_part, name='view_part'),
    path('add_part/', views.add_part, name='add_part'),
    path('edit_part/<int:part_id>/', views.edit_part, name='edit_part'),
    path('delete_part/<int:part_id>/', views.delete_part, name='delete_part'),
]
