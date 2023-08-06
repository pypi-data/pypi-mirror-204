class GenericalException(Exception):
    pass

class ObjectDoesNotExist(Exception):
    def __init__(self, obj_id):
        self.id = obj_id

    def __str__(self):
        return f'Element by id {self.id} does not exist'

class IDRequiredException(ValueError):
    def __str__(self):
        return 'id is required'

class EnvVariablesException(ValueError):
    def __str__(self):
            return 'required environment variables'

class AccessDeniedException(Exception):
    def __str__(self):
            return 'Access Denied, Check your credentials'