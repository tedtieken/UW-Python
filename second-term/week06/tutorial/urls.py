from django.conf.urls.defaults import *
from settings import MEDIA_ROOT

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    #(r'^tutorial/', include('tutorial.foo.urls')),
    (r'^assets/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),

    url(r'^$', 'polls.views.poll_index', name="index"),
    url(r'^polls/$', 'polls.views.poll_index', name="poll_index"),
    url(r'^polls/(?P<poll_id>\d+)/$', 'polls.views.poll_detail', name="poll_detail"),
    url(r'^polls/(?P<poll_id>\d+)/results/$', 'polls.views.poll_results', name="poll_results"),
    url(r'^polls/(?P<poll_id>\d+)/vote/$', 'polls.views.poll_vote', name="poll_vote"),

    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    
    
)
