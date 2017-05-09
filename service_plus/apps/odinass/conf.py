import os

from django.conf import settings as django_settings


class AppSettings(object):
    DELETE_FILES_AFTER_IMPORT = getattr(django_settings,
                                        '1C_DELETE_FILES_AFTER_IMPORT', True)
    FILE_LIMIT = getattr(django_settings, '1C_FILE_LIMIT', 0)
    UPLOAD_ROOT = getattr(django_settings, '1C_UPLOAD_ROOT',
                          os.path.join(django_settings.MEDIA_ROOT, '1c_tmp'))
    USE_ZIP = getattr(django_settings, '1C_USE_ZIP', False)


settings = AppSettings()
