from django.views.generic import DetailView

from templated_docs import fill_template
from templated_docs.http import FileResponse

from crm.models import Booking


class BaseDocumentView(DetailView):
    """
    Базовый класс для документов
    """
    model = Booking
    output_format = None
    visible_filename = None

    def render_to_response(self, context, **response_kwargs):
        context.update({'user': self.request.user})
        file = fill_template(self.template_name, context,
                             output_format=self.output_format)
        return FileResponse(file, self.visible_filename)
