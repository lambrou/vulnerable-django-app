from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', include('django.contrib.auth.urls')),
    path('users/signup/', views.signup, name='signup'),
    path('users/profile', views.profile, name='signup'),
]