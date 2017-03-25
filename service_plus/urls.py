from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import RedirectView, TemplateView

from rest_framework import routers

from crm.views import (
    BrandAutocomplete,
    JobViewSet,
    ModelAutocomplete,
    SparePartCountViewSet,
    SparePartViewSet,
)


router = routers.DefaultRouter()
router.register(r'jobs', JobViewSet)
router.register(r'spare_part', SparePartViewSet)
router.register(r'spare_part_count', SparePartCountViewSet)

urlpatterns = [
    url(r'^$',
        TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^robots.txt$',
        TemplateView.as_view(template_name='robots.txt',
                             content_type='text/plain')),
    url(r'^favicon.ico$',
        RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'),
                             permanent=True)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^autocomplete/brand/$', login_required(BrandAutocomplete.as_view()),
        name='brand-autocomplete',),
    url(r'^autocomplete/model/$', login_required(ModelAutocomplete.as_view()),
        name='model-autocomplete',),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
