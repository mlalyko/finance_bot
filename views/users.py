from models import User


def identify_user(update):
    """ Try to find user in db. If can't - call add_new_user. Return user object. """
    existing_user = User.objects(user_id=update.message.from_user.id)
    existing_user = existing_user.first() if existing_user else None

    if not existing_user:
        existing_user = add_new_user(update)

    return existing_user


def add_new_user(update):
    """ Create new user in db. Return user object. """
    new_user = User(
        user_id=update.message.from_user.id,
        username=update.message.from_user.username,
        first_name=update.message.from_user.first_name,
        last_name=update.message.from_user.last_name,
    )

    new_user.save()
    return new_user
