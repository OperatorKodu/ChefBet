from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('main/', views.main, name='main'),
    path('category/<str:category_name>/', views.category, name='category'),
    path('more/<int:event_id>/', views.more, name='more'),
    #path('my_coupons/', views.my_coupons, name='my_coupons'),
]