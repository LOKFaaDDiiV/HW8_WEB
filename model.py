from mongoengine import Document, connect
from mongoengine.fields import StringField, BooleanField

connect(host='mongodb+srv://lokfaaddiiv:admin@lokfaaddiiv.pdegaqw.mongodb.net/contacts?retryWrites=true&w=majority')


class Contact(Document):
    fullname = StringField()
    email = StringField()
    phone = StringField()
    preferred = StringField()
    is_delivered = BooleanField(default=False)
