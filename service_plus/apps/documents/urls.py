from django.conf.urls import url

from documents import views as docs_views


urlpatterns = [
    url(r'^(?P<pk>\d+)/done/$', docs_views.BaseDocumentView.as_view(
            template_name='documents/done.odt', output_format='pdf',
            visible_filename='done.pdf'),
        name='done_document'),
]
