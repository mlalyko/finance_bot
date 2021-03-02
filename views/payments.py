from telegram.ext import ConversationHandler
from models import Payment
import keyboards
from views.common_handlers import handle_error
from views.users import identify_user

# need to conversation handler, like some states
CATEGORY, CONFIRMATION = 1, 2


def handle_new_payment(update, context):
    """ Get payment message, collect info about payment and go to next entry choose_category"""
    received_message = update.effective_message.text

    try:
        context.user_data['price'], context.user_data['payment_info'] = define_price_and_payment_info(received_message)
    except TypeError:
        handle_error(update, 'Failed to determine the cost')
    else:
        existing_user = identify_user(update)
        update.message.reply_text('Choose category', reply_markup=keyboards.create_category_keyboard(existing_user))
        return CATEGORY


def choose_category(update, context):
    """ Get category of payment from user and call add_payment_in_db """
    received_message = update.effective_message.text
    existing_user = identify_user(update)

    if received_message in ('Blocks', 'Stable spendings'):
        update.message.reply_text('Choose category',
                                  reply_markup=keyboards.create_category_keyboard(existing_user, received_message))
    else:
        try:
            context.user_data['category'] = [i.name for i in existing_user.categories if i.name == received_message[2:]][0]
        except IndexError:
            handle_error(update, 'Can\'t define category')
        else:
            text = (f'Your payment: {context.user_data["payment_info"]} {context.user_data["price"]} rub in '
                    f'{context.user_data["category"]}\nAlways, ok?')
            update.message.reply_text(text, reply_markup=keyboards.ok_kb)
            return CONFIRMATION


def payment_data_confirmation(update, context):
    """ Handle user confirmation of data about payment """
    received_message = update.effective_message.text

    if received_message == 'Ok':
        add_payment_in_db(update, context)

    update.message.reply_text('So good!' if received_message == 'Ok' else 'Try again please')
    return ConversationHandler.END


def add_payment_in_db(update, context):
    """ Add new record with payment in db """
    existing_user = identify_user(update)

    new_payment = Payment(
        price=context.user_data['price'],
        payment_info=context.user_data['payment_info'],
        category=context.user_data['category']
    )

    existing_user.payments.append(new_payment)
    existing_user.save()


def define_price_and_payment_info(message):
    """ Define price and payment information from user message. Return tuple with data. """
    try:
        price = max([int(i) for i in message.split() if i.isdigit()])
    except ValueError:
        return None

    payment_info = message.replace(str(price), '')

    return price, payment_info


