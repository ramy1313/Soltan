from django.conf.urls import patterns, include, url
import settings
from django.conf.urls.static import static
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('members.views',
    url(r'^members/$', 'index'),
    url(r'^members/(?P<member_id>\d+)/$', 'detail'),
    url(r'^members/add_member/$', 'add_member'),
    url(r'^members/fee/$', 'fee'),
    url(r'^members/Q_member_search/$', 'q_member_search'),
    url(r'^members/(?P<membership_id>\d+)/pay_receipt/$', 'pay_receipt'),
    url(r'^members/(?P<member_id>\d+)/edit_member/$', 'edit_member'),
    url(r'^members/(?P<member_id>\d+)/delete_member/$', 'delete_member'),
    url(r'^members/(?P<member_id>\d+)/deactivate/$', 'deactivate'),
    url(r'^members/(?P<member_id>\d+)/activate/$', 'activate'),
    url(r'^members/(?P<member_id>\d+)/rec_list/$', 'rec_list'),
    url(r'^members/(?P<rec_id>\d+)/rec_detail/$', 'rec_detail'),
    url(r'^members/(?P<rec_id>\d+)/del_rec/$', 'del_rec'),
)

urlpatterns += patterns('cases.views',
    url(r'^cases/(?P<case_id>\d+)/$', 'detail'),
    url(r'^cases/add_case/$', 'add_case'),
)

urlpatterns += patterns('',
    # Examples:
    # url(r'^$', 'soltan.views.home', name='home'),
    # url(r'^soltan/', include('soltan.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', direct_to_template, {"template": "home.html"}),
    url(r'^login/$', 'soltan_login.views.soltan_login'),
    url(r'^logout/$', 'soltan_login.views.soltan_logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
