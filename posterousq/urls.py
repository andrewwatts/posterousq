
from django.conf import settings
from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns


handler404 = 'posterousq.views.not_found'

urlpatterns = patterns('posterousq.views',
    (r'^form$',                 'form'),
    (r'^form/(?P<id>\d+)',      'form'),
    (r'^post$',                 'post'),
    (r'^post/(?P<id>\d+)',      'post'),
)

# direct to template
urlpatterns += patterns('django.views.generic.simple',
    (r'^$',                     'direct_to_template',   {'template': 'posterousq/calendar.html'}),
)

# do admin and static media in development
if settings.DEBUG is True:
    #enable admin
    from django.contrib import admin
    admin.autodiscover()
    urlpatterns += patterns('',
        (r'^admin/',         include(admin.site.urls)),
    )
    #enable static media
    urlpatterns += patterns('django.views.static',
        (r'^media/(?P<path>.*)$',   'serve',                {'document_root': settings.MEDIA_ROOT}),
    )
