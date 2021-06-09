from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:page>/', views.subpages, name='subpage'),
    path('more/<int:event_id>/', views.more, name='more'),
    #path('my_coupons/', views.my_coupons, name='my_coupons'),
]