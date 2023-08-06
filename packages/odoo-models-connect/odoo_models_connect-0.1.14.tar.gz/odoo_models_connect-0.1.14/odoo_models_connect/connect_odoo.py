import xmlrpc.client


class ConnectOdoo(object):
    """This class manages the whole process of connection
    with odoo to create microservices from it
    or just make simple queries if required.
    """

    username = None
    password = None
    uid = None

    def __init__(self, url: str, db: str):
        self.__url = url
        self.__db = db
        self.__models = xmlrpc.client.ServerProxy(
            '{}/xmlrpc/2/object'.format(url))
        self.__common = xmlrpc.client.ServerProxy(
            '{}/xmlrpc/2/common'.format(url))

    def authenticate(self, email: str, password: str):
        """authenticates the user in the odoo system with email and password.

        Args:
            email (str): user email.
            password (str): user password.

        Returns:
            float: authenticated user id
        """
        uid = self.__common.authenticate(self.__db, email, password, {})
        if uid is not False:
            self.username = email
            self.password = password
            self.uid = uid
        return uid

    def reconnect(self, obj: dict):
        """this function is used when you have saved the credentials of the user who is logged ind
        and you need to make a query to the odoo system.

        Args:
            obj (dict): the obj is a dictionary that must contain the user's data:
            id, username or email and password.
        """
        self.username = obj['username']
        self.password = obj['password']
        self.uid = obj['uid']

    def search_read(self, model_name: str, condition: list = [], fields: list = []):
        """this function makes a query to the specified odoo model,
        returning a list of dictionaries with the specified data.

        Args:
            model_name (str): name of the odoo model to which the query will be made.
            condition (list, optional): condition or filter to be applied to the query.
                Example: odoo.search_read('res.users', condition=[['id', '=', 8]]). Defaults to [].
            fields (list, optional): fields that will be brought from the model,
                by default always brings the id field. Defaults to [].

        Returns:
            list: a list of items brought from the query.
        """
        data = self.__models.execute_kw(
            self.__db,
            self.uid,
            self.password,
            model_name,
            'search_read',
            [condition],
            {'fields': fields}
        )
        return data

    def read(self, model_name: str, object_ids: list, fields: list = []):
        """this function allows to search a model with a list of ids of the elements to be searched.

        Args:
            model_name (str): name of the odoo model to which the query will be made.
            object_ids (list): list of ids of the elements to be searched.
            fields (list, optional): fields that will be brought from the model,
                by default always brings the id field. Defaults to [].

        Returns:
            list: list of dictionaries with the data found.
        """
        data = self.__models.execute_kw(
            self.__db,
            self.uid,
            self.password,
            model_name,
            'read',
            [object_ids],
            {'fields': fields}
        )
        return data

    def search_ids(self, model_name: str, domain: list = []):
        """this function gets all the ids that match the condition,
        if no condition is set it will get all the ids of the elements in the model

        Args:
            model_name (str): name of the odoo model to which the query will be made.
            domain (list, optional): condition to be applied to the query. Defaults to [].

        Returns:
            list: list of ids of the elements
        """
        data = self.__models.execute_kw(
            self.__db,
            self.uid,
            self.password,
            model_name,
            'search',
            [domain],
        )
        return data

    def create(self, model_name: str, data: dict):
        """this function creates an existing object using a dictionary with the values that will be assigned to it.

        Args:
            model_name (str): name of the odoo model to which the query will be made.
            data (dict): dictionary with the values to be assigned to the created object.
        """
        self.__models.execute_kw(
            self.__db,
            self.uid,
            self.password,
            model_name,
            'create',
            [data]
        )

    def write(self, model_name: str, object_id: int, data: dict):
        """this function updates an existing object using its id and a dictionary with new values.

        Args:
            model_name (str): name of the odoo model to which the query will be made.
            object_id (int): id of the object to be updated.
            data (dict): dictionary with the values to be assigned to the updated object.
        """
        self.__models.execute_kw(
            self.__db,
            self.uid,
            self.password,
            model_name,
            'write',
            [[int(object_id)], data]
        )

    def delete(self, model_name: str, object_id: int):
        """this function removes an object from the database using its id.

        Args:
            model_name (str): name of the odoo model to which the query will be made.
            object_id (int): id of the object to be deleted.
        """
        self.__models.execute_kw(
            self.__db,
            self.uid,
            self.password,
            model_name,
            'unlink',
            [[int(object_id)]]
        )
