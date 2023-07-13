from rest_framework.response import Response
from rest_framework import exceptions, status
from rest_framework.views import set_rollback, Http404, PermissionDenied

def exception_handler(exc, context):
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait
        data = exc.detail
        set_rollback()
        return Response(
            {
                'code': 1,
                'message': data,
            },
            status=status.HTTP_200_OK,
            headers=headers
        )

    return None
