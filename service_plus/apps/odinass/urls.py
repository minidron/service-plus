from django.conf.urls import url

from odinass.views import FrontView


urlpatterns = [
    url(r'^exchange$', FrontView.as_view(), name='exchange'),
]
