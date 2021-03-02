from models import Category
from views.users import identify_user


def add_categories(update, context):
    """ Add new categories in DB """
    received_message = update.effective_message.text

    categories_from_message = received_message.split(' ', 1)[1].split(', ')
    for cat in categories_from_message[1:]:
        new_cat = Category(name=cat.capitalize(), category_type=categories_from_message[0])
        user = identify_user(update)
        user.categories.append(new_cat)
        user.save()