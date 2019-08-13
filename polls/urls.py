from django.conf.urls import *
from polls import views

app_name="polls"

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
        url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
        url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
        url(r'^profile/(?P<user_id>\d+)/$', views.profil, name='profile'),
]