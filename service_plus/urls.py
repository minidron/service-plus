from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic import RedirectView, TemplateView

from rest_framework import routers

from crm import views as crm_views


router = routers.DefaultRouter()
router.register(r'jobs', crm_views.JobViewSet)
router.register(r'spare_part', crm_views.SparePartViewSet)
router.register(r'spare_part_count', crm_views.SparePartCountViewSet)

urlpatterns = [
    url(r'^$', crm_views.FrontpageView.as_view(), name='index'),
    url(r'^robots.txt$',
        TemplateView.as_view(template_name='robots.txt',
                             content_type='text/plain')),
    url(r'^favicon.ico$',
        RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'),
                             permanent=True)),
    url(r'^admin/docs/', include('documents.urls', namespace='documents')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^1c/', include('odinass.urls', namespace='1c')),
    url(r'^api/', include(router.urls)),
    url(r'^autocomplete/brand/$',
        login_required(crm_views.BrandAutocomplete.as_view()),
        name='brand-autocomplete',),
    url(r'^autocomplete/model/$',
        login_required(crm_views.ModelAutocomplete.as_view()),
        name='model-autocomplete',),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
