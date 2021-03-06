"""paiementmandat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# from django.conf.urls import url
# from django.contrib import admin
#
# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
# ]


from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^partner/', include('teyco.urls')),
    #url(r'^courses/', include('courses.urls')),
    url(r'^password/reset/$', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('auth_password_reset_done'),html_email_template_name='registration/password_reset_email.html')
, name='auth_password_reset'),
    url(r'^$', auth_views.login, name='login'),
    #url(r'^accueil/$', courses.views.home, name='home'),
    url(r'^accounts/', include('registration.backends.default.urls')),
]
