from mongoengine import Document, ListField, StringField, ReferenceField


class Authors(Document):
    full_name = StringField(required=True, unique=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()
    meta = {'allow_inheritance': True}


class Quotes(Document):
    tags = ListField(StringField())
    author = ReferenceField(Authors, reverse_delete_rule=2)
    quote = StringField()
    meta = {'allow_inheritance': True}


