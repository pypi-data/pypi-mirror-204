class OdooField(object):
    _type = None

class StringField(OdooField):
    _type = 'char'

class BooleanField(OdooField):
    _type = 'bool'

class BinaryField(OdooField):
    _type = 'binary'

class DateField(OdooField):
    _type = 'date'

class DateTimeField(OdooField):
    _type = 'datetime'

class IntegerField(OdooField):
    _type = 'integer'

class FloatField(OdooField):
    _type = 'float'

class MonetaryField(OdooField):
    _type = 'monetary'

class Many2oneField(OdooField):
    _type = 'many2one'

class Many2manyField(OdooField):
    _type = 'many2many'

class One2manyField(OdooField):
    _type = 'one2many'
