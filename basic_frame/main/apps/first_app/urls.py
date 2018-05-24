from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^$', views.index), #template for registration
    url(r'^users$', views.index), #template for registration
    url(r'^users/(?P<id>\d+)$', views.show), #template for user's graphs
    url(r'^users/login_page$', views.login_page), #template for login
    url(r'^users/(?P<id>\d+)/edit$', views.edit_page),#edit user template
    url(r'^graphs$', views.dashboard), #graph homepage
    url(r'^graphs/dashboard/(?P<user_id>\d+)$', views.graph_interface), #the page that shows the making a graph interface
    #------POSTS------------
    url(r'^users/logout$', views.logout), #clears session
    url(r'^users/add$', views.create), #post create user
    url(r'^users/edit$', views.edit_user), #edit user and validate the post data
    url(r'^graphs/add/(?P<user_id>\d+)$', views.addquote), #posts a quote from dashboard
    url(r'^graphs/delete/(?P<quote_id>\d+)$', views.delquote), #posts a quote from dashboard
    url(r'^graphs/like/(?P<user_id>\d+)/(?P<quote_id>\d+)$', views.like), #posts a quote from dashboard
    #-------VALIDATIONS------
    url(r'^users/login$', views.login) #login validation
    #url(r'^users/(?P<id>\d+)/delete$', views.destroy) #post
]
