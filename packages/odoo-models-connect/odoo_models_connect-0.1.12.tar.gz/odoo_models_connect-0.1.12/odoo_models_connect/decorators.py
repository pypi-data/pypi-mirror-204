from .exceptions import (
    GenericalException,
    AccessDeniedException,
)

def access_denied(method):
    def wrapper(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except xmlrpc.client.Fault as error:
            if error.faultCode == 3:
                raise AccessDeniedException()
            else:
                raise GenericalException("Error Fault capturado: Código de error: %d. Mensaje de error: %s" % (error.faultCode, error.faultString))
    return wrapper