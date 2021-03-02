from mongoengine import *
from decouple import config


connect(config('DATABASE'))


class Category(EmbeddedDocument):
    category_type = StringField(choices=['Stable spendings', 'Blocks'], null=True, blank=True)
    name = StringField()
    icon = StringField(default='•')

    def __str__(self):
        return f'{self.icon} {self.name}'


class Payment(EmbeddedDocument):
    price = IntField()
    payment_info = StringField()
    category = StringField()

    def __str__(self):
        return f'{self.payment_info[:10]}...: {self.price}'


class User(Document):
    first_name = StringField()
    last_name = StringField()
    username = StringField()
    user_id = IntField()
    is_admin = BooleanField(default=False)
    categories = ListField(EmbeddedDocumentField(Category))
    payments = ListField(EmbeddedDocumentField(Payment))

    def __str__(self):
        name = ''
        for i in self.first_name, self.last_name, self.username:
            if i:
                name += f' {i}'
        return name

