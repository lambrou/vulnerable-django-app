from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', include('django.contrib.auth.urls')),
    path('users/changepass', views.changepass, name='changepass'),
    path('users/signup', views.signup, name='signup'),
    path('users/profile', views.profile, name='signup'),
    path('utils/testconn', views.testconn, name='testconn'),
    path('utils/filerunner', views.filerunner, name='filerunner'),
]