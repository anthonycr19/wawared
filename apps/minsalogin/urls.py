from django.conf.urls import url

from . import views

app_name = 'minsalogin'
urlpatterns = [
    url(r'^accounts/login/$', views.MinsaLoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', views.MinsaLogoutView.as_view(), name='logout'),
    url(r'^accounts/establecimiento/$', views.MinsaLoginChooseEstablishment.as_view(),
        name='choose_establishment'),
    url(r'^403/$', views.Error403.as_view(), name='error403'),
]
