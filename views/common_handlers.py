from telegram.ext import ConversationHandler


def handle_error(update, error_message):
    update.message.reply_text(error_message)


def cancel_operation(update, context):
    update.message.reply_text('Operation was cancelled')
    return ConversationHandler.END

