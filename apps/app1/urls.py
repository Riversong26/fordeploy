from django.conf.urls import re_path
from . import views        
urlpatterns = [
    re_path(r'^$', views.index),
    re_path(r'^registration_process$', views.registration_process),
    re_path(r'^login_process$', views.login_process),
    re_path(r'^logout$', views.logout),    
    re_path(r'^pokes$', views.pokes),
    re_path(r'^pokes/(?P<user_id>\d+)/more$', views.more)
]                
