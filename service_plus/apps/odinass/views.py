import os
import logging

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import Http404, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from odinass.conf import settings as odinass_settings


logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class FrontView(View):
    def __init__(self, **kwargs):
        self.routes_map = {
            ('catalog', 'checkauth'): 'check_auth',
            ('catalog', 'file'): 'upload_file',
            ('catalog', 'import'): 'import_file',
            ('catalog', 'init'): 'init',
            ('sale', 'checkauth'): 'check_auth',
            ('sale', 'query'): 'export_query',
            ('sale', 'success'): 'export_success',
            # ('import', 'import'): import_file,
            # ('sale', 'file'): upload_file,
            # ('sale', 'init'): init,
        }
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        method_name = self.routes_map.get((request.GET.get('type'),
                                           request.GET.get('mode')))
        if not method_name:
            raise Http404

        method = getattr(self, method_name, None)
        if not method:
            raise Http404

        return method(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def success(self, success_text=''):
        result = '{}\n{}'.format('success', success_text)
        return HttpResponse(result)

    def error(self, error_text=''):
        result = '{}\n{}'.format('failure', error_text)
        return HttpResponse(result)

    def check_auth(self, request, *args, **kwargs):
        session = request.session
        session.create()
        success_text = '{}\n{}'.format(settings.SESSION_COOKIE_NAME,
                                       session.session_key)
        return self.success(success_text)

    def init(self, request, *args, **kwargs):
        result = 'zip={}\nfile_limit={}'.format(
            'yes' if odinass_settings.USE_ZIP else 'no',
            odinass_settings.FILE_LIMIT)
        return HttpResponse(result)

    def upload_file(self, request, *args, **kwargs):
        try:
            filename = os.path.basename(request.GET['filename'])
        except KeyError:
            return self.error('Filename param required')

        if not os.path.exists(odinass_settings.UPLOAD_ROOT):
            try:
                os.makedirs(odinass_settings.UPLOAD_ROOT)
            except OSError:
                return self.error('Can\'t create upload directory')

        temp_file = SimpleUploadedFile(filename, request.read(),
                                       content_type='text/xml')

        with open(os.path.join(odinass_settings.UPLOAD_ROOT,
                               filename), 'wb') as f:
            for chunk in temp_file.chunks():
                f.write(chunk)
        return self.success()

    def import_file(self, request, *args, **kwargs):
        try:
            filename = os.path.basename(request.GET['filename'])
        except KeyError:
            return self.error('Filename param required')

        file_path = os.path.join(odinass_settings.UPLOAD_ROOT, filename)
        if not os.path.exists(file_path):
            return self.error('%s doesn\'t exist' % filename)

        # DO IMPORT FILES

        if odinass_settings.DELETE_FILES_AFTER_IMPORT:
            try:
                os.remove(file_path)
            except OSError:
                logger.error('Can\'t delete %s after import' % filename)
        return self.success()

    def export_query(self, request, *args, **kwargs):
        # DO EXPORT

        file_path = os.path.join(odinass_settings.UPLOAD_ROOT, 'test.xml')
        io = open(file_path, 'r')
        return HttpResponse(io.read(), content_type='text/xml')

    def export_success(self, request, *args, **kwargs):
        return self.success()
