from django.conf.urls import url

from documents import views as docs_views


urlpatterns = [
    url(r'^(?P<pk>\d+)/receipt/$', docs_views.BaseDocumentView.as_view(
            template_name='documents/receipt.odt', output_format='pdf',
            visible_filename='receipt.pdf'),
        name='receipt'),
    url(r'^(?P<pk>\d+)/guarantee/$', docs_views.BaseDocumentView.as_view(
            template_name='documents/done.odt', output_format='pdf',
            visible_filename='done.pdf'),
        name='guarantee'),
]
