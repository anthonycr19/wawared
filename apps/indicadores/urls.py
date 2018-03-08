# -*- coding: utf-8 -*-
# Python imports


# Django imports
from django.conf.urls import url

# Third party apps imports


# Local imports
from .views import IndexFormView

# Create your tests here.


urlpatterns = [
    url(
        r'^$',
        IndexFormView.as_view(),
        name='index'
    ),
]
