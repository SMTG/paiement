from django.conf.urls import url
from . import views


#app_name = 'blog'
urlpatterns = [
    url(r'^$', views.home, name='home'),
url(r'^charger-mandat/$', views.charger_mandat, name='charger_mandat'),
url(r'^search-form/$', views.search, name='search_mandat'),
url(r'^(?P<id>\d+)/(?P<user_id>\d+)$', views.mandat_pdf, name='mandat_pdf'),
url(r'^rapport_jour_pdf/(?P<user_id>\d+)$', views.rapport_jour_pdf, name='rapport_jour_pdf'),
#url(r'^rapport_periode_pdf/(?P<user_id>\d+)$', views.rapport_periode_pdf, name='rapport_periode_pdf'),
url(r'^search-periodique/(?P<user_id>\d+)$', views.rapport_periodique, name='rapport_periodique'),
]