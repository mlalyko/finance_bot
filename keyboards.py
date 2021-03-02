from telegram import ReplyKeyboardMarkup


def create_category_keyboard(user, keyboard_type='Stable spendings'):
    """
    Create keyboard with categories from user.categories
    :param user: user object
    :param keyboard_type: need to add alternative keyboard button
    :return: keyboard object
    """
    user_categories = user.categories
    kb_list = []
    row = []
    alternative_kb = 'Blocks' if keyboard_type == 'Stable spendings' else 'Stable spendings'
    for category in user_categories:
        if category.category_type != alternative_kb:
            row.append(f'{category.icon} {category.name}')
            if len(row) == 3:
                kb_list.append(row)
                row = []

    kb_list.append(row)
    kb_list[-1].append(alternative_kb)

    return ReplyKeyboardMarkup(kb_list, resize_keyboard=True, one_time_keyboard=True)


ok_kb = ReplyKeyboardMarkup([['Ok', 'Something wrong']], resize_keyboard=True, one_time_keyboard=True)
