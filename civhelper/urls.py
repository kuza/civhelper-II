from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from civ import views

urlpatterns = patterns('',
#    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.HomePageView.as_view(), name='home'),
)
