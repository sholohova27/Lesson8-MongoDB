import mongoengine as m


class Author(m.Document):
    fullname = m.StringField(required=True)
    born_date = m.StringField()
    born_location = m.StringField()
    description = m.StringField()


class Quote(m.Document):
    tags = m.ListField(m.StringField())
    author = m.ReferenceField(Author, reverse_delete_rule=m.CASCADE)
    quote = m.StringField(required=True)
