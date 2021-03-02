from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters, CallbackQueryHandler
from views import common_handlers, payments, categories
from decouple import config


def main():
    print('Start')
    updater = Updater(token=config('TG_TOKEN'), use_context=True)
    dp = updater.dispatcher.add_handler

    # categories
    dp(CommandHandler('add_categories', categories.add_categories))

    # payments
    dp(ConversationHandler(
        entry_points=[CommandHandler('payments', payments.send_choose_kb)],
        states={
            payments.CATEGORY: [MessageHandler(Filters.text, payments.choose_category)],
        },
        fallbacks=[CommandHandler('stop', common_handlers.cancel_operation)]
    ))

    dp(ConversationHandler(
        entry_points=[MessageHandler(Filters.text, payments.handle_new_payment)],
        states={
            payments.CATEGORY: [MessageHandler(Filters.text, payments.choose_category)],
            payments.CONFIRMATION: [MessageHandler(Filters.text, payments.payment_data_confirmation)]
        },
        fallbacks=[CommandHandler('stop', common_handlers.cancel_operation)]
    ))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
