from django.conf.urls import url
from django.contrib import admin
from Oriana import views

urlpatterns = [

    url(r'^$', views.dashboard),
    url(r'^admin/', admin.site.urls),

    url(r'^hosts/', views.hosts),
    url(r'^shosts/', views.shosts),
    url(r'^users/', views.users),
    url(r'^services/$', views.services),
    url(r'^tasks/$', views.tasks),
    url(r'^dashboard/', views.dashboard),

    url(r'^host/(?P<host_id>\d+)/$', views.host),
    url(r'^shost/(?P<shost_id>\d+)/$', views.shost),
    url(r'^user/(?P<user_id>\d+)/$', views.user),
    url(r'^service/(?P<service_id>\d+)/$', views.service),
    url(r'^task/(?P<task_id>\d+)/$', views.task),

    url(r'^possible_lm/', views.possible_lm),
    url(r'^possible_lm_detail/(?P<possiblelm_id>\d+)/$', views.possible_lm_detail),
    url(r'^lm_sessions/', views.lm_sessions),
    url(r'^lmsession/(?P<lmsession_id>\d+)/$', views.lmsession),

    url(r'^fa_cmdline/$', views.fa_cmdline),
    url(r'^fa_cmdline/(?P<cmdline_id>\d+)/$', views.fa_cmdline_detail),

    url(r'^suspicious_behavior/$', views.suspicious_behavior),
    url(r'^suspicious_behavior/(?P<type>[\w: \/&-]+)/$', views.suspicious_behavior_type),

    url(r'^suspicious_user_behavior/$', views.suspicious_user_behavior),
    url(r'^suspicious_user_behavior/(?P<user_id>\d+)/$', views.suspicious_behavior_user),
    url(r'^suspicious_user_behavior_detail/(?P<s_id>\d+)/$', views.suspicious_user_behavior_detail),

    url(r'^suspicious_source_behavior/$', views.suspicious_source_behavior),
    url(r'^suspicious_source_behavior/(?P<source_id>\d+)/$', views.suspicious_behavior_source),
    url(r'^suspicious_source_behavior_detail/(?P<s_id>\d+)/$', views.suspicious_source_behavior_detail),

]
