from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'events', views.EventsViewSet)
router.register(r'coupons', views.CouponsViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', views.main, name='main'),
    path('main/', views.main, name='main'),
    path('category/<str:category_name>/', views.category, name='category'),
    path('more/<int:event_id>/', views.more, name='more'),
    path('signup/', views.signup, name='signup'),
    url(r"^accounts/", include("django.contrib.auth.urls")),
    path('test/', views.test, name='test'),
    path('', include(router.urls)),
]
