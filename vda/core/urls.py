from django.contrib.auth import views as auth_views

from django.urls import include, path
from . import views
import configparser
config = configparser.ConfigParser()
config.read('core/static/core/navinfo.ini')

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', include('django.contrib.auth.urls')),
    path('users/login', auth_views.LoginView.as_view(extra_context = {'navinfo': config['DEFAULT']['BruteForce']})),
    path('users/changepass', views.changepass, name='changepass'),
    path('users/signup', views.signup, name='signup'),
    path('users/profile', views.profile, name='signup'),
    path('utils/testconn', views.testconn, name='testconn'),
    path('utils/filerunner', views.filerunner, name='filerunner'),
    path('utils/userlookup', views.userlookup, name='userlookup'),
    path('utils/guestbook', views.guestbook, name='guestbook'),
]