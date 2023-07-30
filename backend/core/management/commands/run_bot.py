import logging
from environs import Env

from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

END = ConversationHandler.END

CUSTOMIZATION, STANDARD_CAKE, ABOUT_US, SELECTING_ACTION = map(chr, range(4))

START_OVER, SHOWING, STOPPING, CUSTOM_CAKE = map(chr, range(4, 8))

TOPPING, BERRIES, DECOR, INSCRIPTION, COMMENT, QUANTITY_LEVEL, FORM, BACK = map(chr, range(8, 16))


def start(update: Update, context: CallbackContext) -> str:
    """Select an action: Adding parent/child or show data."""

    text = (
        "Вы можете заказать готовый торт или сконструировать его! "
        " Чтобы остановить работу бота, просто введите  /stop"
    )

    buttons = [
        [
            InlineKeyboardButton(text='Кастомизация торта', callback_data=str(CUSTOMIZATION)),
            InlineKeyboardButton(text='Готовые варианты', callback_data=str(STANDARD_CAKE)),
            InlineKeyboardButton(text='О нас', callback_data=str(ABOUT_US)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    # If we're starting over we don't need to send a new message
    if context.user_data.get(START_OVER):
        update.callback_query.answer()
        update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        update.message.reply_text(
            "Привет, я BakeCake Бот и я помогу вам заказать торт"
        )
        update.message.reply_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False

    return SELECTING_ACTION


def create_custom_cake(update: Update, context: CallbackContext) -> str:
    """Choose to add mother or father."""

    text = 'Пожалуйста выберите, что добавить'

    buttons = [
        [
            InlineKeyboardButton(text='Уровни', callback_data=str(QUANTITY_LEVEL)),
            InlineKeyboardButton(text='Форма', callback_data=str(FORM)),
            InlineKeyboardButton(text='Топпинг', callback_data=str(TOPPING)),
        ],
        [
            InlineKeyboardButton(text='Ягоды', callback_data=str(BERRIES)),
            InlineKeyboardButton(text='Декор', callback_data=str(DECOR)),
            InlineKeyboardButton(text='Надпись', callback_data=str(INSCRIPTION)),
        ],
        [
            InlineKeyboardButton(text='Комментарий', callback_data=str(COMMENT)),
            InlineKeyboardButton(text='Информация', callback_data=str(SHOWING)),
            InlineKeyboardButton(text='Назад', callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False

    return CUSTOM_CAKE


def standard_cake(update: Update, context: CallbackContext) -> str:
    """Choose to add mother or father."""

    text = 'Пожалуйста выберите готовые варианты'

    buttons = [
        [
            InlineKeyboardButton(text='Информация', callback_data=str(SHOWING)),
            InlineKeyboardButton(text='Назад', callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False

    return STANDARD_CAKE


def about_us(update: Update, context: CallbackContext) -> str:
    """Handle the selection of cake topping."""

    telegram = "@BakeCakePy_bot"
    instagram = "https://www.instagram.com"
    phone_number = "8-954-424-90-09"
    address = "Пресненская наб., 8 стр 1, Москва, 123112"

    text = (
        f"Ссылка на Telegram: {telegram}\n"
        f"Ссылка на Instagram: {instagram}\n"
        f"Номер телефона: {phone_number}\n"
        f"Адрес: {address}"
    )

    buttons = [
        [
            InlineKeyboardButton(text='Назад', callback_data=str(END)),
        ],
    ]

    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False

    return ABOUT_US


def end_second_level(update: Update, context: CallbackContext) -> int:
    """Return to top level conversation."""
    context.user_data[START_OVER] = True
    start(update, context)

    return END


def handle_quantity_level_selection(update: Update, context: CallbackContext) -> str:
    """Handle the selection of quantity levels for the cake."""
    text = "Выберите количество уровней:"

    buttons = [
        [
            InlineKeyboardButton(text='1 уровень', callback_data='1'),
            InlineKeyboardButton(text='2 уровня', callback_data='2'),
            InlineKeyboardButton(text='3 уровня', callback_data='3'),
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False

    return CUSTOM_CAKE


def handle_cake_form_selection(update: Update, context: CallbackContext) -> str:
    """Handle the selection of cake form."""
    text = "Выберите форму торта:"

    buttons = [
        [
            InlineKeyboardButton(text='Круглая', callback_data='round'),
            InlineKeyboardButton(text='Прямоугольная', callback_data='rectangular'),
            InlineKeyboardButton(text='Квадратная', callback_data='square'),
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False

    return CUSTOM_CAKE


def handle_topping_selection(update: Update, context: CallbackContext) -> str:
    """Handle the selection of cake topping."""
    text = "Выберите топпинг для торта:"

    buttons = [
        [
            InlineKeyboardButton(text='Шоколадный', callback_data='chocolate'),
            InlineKeyboardButton(text='Карамельный', callback_data='caramel'),
            InlineKeyboardButton(text='Фруктовый', callback_data='fruit'),
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False

    return CUSTOM_CAKE


def handle_berries_selection(update: Update, context: CallbackContext) -> str:
    """Handle the selection of cake topping."""
    text = "Выберите ягоды для добавления:"

    buttons = [
        [
            InlineKeyboardButton(text='Клубника', callback_data='strawberries'),
            InlineKeyboardButton(text='Голубика', callback_data='blueberries'),
            InlineKeyboardButton(text='Малина', callback_data='raspberries'),
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False

    return CUSTOM_CAKE


def handle_decor_selection(update: Update, context: CallbackContext) -> str:
    """Handle the selection of cake topping."""
    text = "Выберите декор для добавления:"

    buttons = [
        [
            InlineKeyboardButton(text='Цветные конфеты', callback_data='sprinkles'),
            InlineKeyboardButton(text='Цветные маршмеллоу', callback_data='marshmallows'),
            InlineKeyboardButton(text='Сахарные цветы', callback_data='sugar_flowers'),
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data=str(END)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False

    return CUSTOM_CAKE


def handle_inscription_selection(update: Update, context: CallbackContext) -> str:
    """Handle the selection of cake topping."""
    text = "Введите текст надписи для торта:"

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)

    context.user_data[START_OVER] = False

    return CUSTOM_CAKE


def handle_comment_selection(update: Update, context: CallbackContext) -> str:
    """Handle the selection of cake topping."""
    text = "Введите текст с комментарием к торту:"

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)

    context.user_data[START_OVER] = False

    return CUSTOM_CAKE


def handle_showing_selection(update: Update, context: CallbackContext) -> str:
    """Handle the selection of cake topping."""
    text = "Тут будет информация:"

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)

    context.user_data[START_OVER] = False

    return CUSTOM_CAKE


def stop(update: Update, context: CallbackContext) -> int:
    """End Conversation by command."""
    update.message.reply_text('До встречи!')

    return END


def main() -> None:
    """Run the bot."""
    env = Env()
    env.read_env()
    tg_bot_token = env('TG_BOT_TOKEN')

    updater = Updater(tg_bot_token)

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CallbackQueryHandler(start, pattern='^' + str(END) + '$'),
            CallbackQueryHandler(create_custom_cake, pattern='^' + str(CUSTOMIZATION) + '$'),
            CallbackQueryHandler(standard_cake, pattern='^' + str(STANDARD_CAKE) + '$'),
            CallbackQueryHandler(about_us, pattern='^' + str(ABOUT_US) + '$'),
            CallbackQueryHandler(end_second_level, pattern='^' + str(BACK) + '$'),
        ],
        states={
            SELECTING_ACTION: [
                CallbackQueryHandler(create_custom_cake, pattern='^' + str(CUSTOMIZATION) + '$'),
                CallbackQueryHandler(standard_cake, pattern='^' + str(STANDARD_CAKE) + '$'),
                CallbackQueryHandler(about_us, pattern='^' + str(ABOUT_US) + '$'),
            ],
            CUSTOM_CAKE: [
                CallbackQueryHandler(end_second_level, pattern='^' + str(END) + '$'),
                CallbackQueryHandler(stop, pattern='^' + str(STOPPING) + '$'),
                CallbackQueryHandler(handle_quantity_level_selection, pattern='^' + str(QUANTITY_LEVEL) + '$'),
                CallbackQueryHandler(handle_cake_form_selection, pattern='^' + str(FORM) + '$'),
                CallbackQueryHandler(handle_topping_selection, pattern='^' + str(TOPPING) + '$'),
                CallbackQueryHandler(handle_berries_selection, pattern='^' + str(BERRIES) + '$'),
                CallbackQueryHandler(handle_decor_selection, pattern='^' + str(DECOR) + '$'),
                CallbackQueryHandler(handle_inscription_selection, pattern='^' + str(INSCRIPTION) + '$'),
                CallbackQueryHandler(handle_comment_selection, pattern='^' + str(COMMENT) + '$'),
                CallbackQueryHandler(handle_showing_selection, pattern='^' + str(SHOWING) + '$'),
            ],
            STANDARD_CAKE: [
                CallbackQueryHandler(end_second_level, pattern='^' + str(END) + '$'),
                CallbackQueryHandler(stop, pattern='^' + str(STOPPING) + '$'),
                CallbackQueryHandler(handle_showing_selection, pattern='^' + str(SHOWING) + '$'),
            ],
            ABOUT_US: [
                CallbackQueryHandler(end_second_level, pattern='^' + str(END) + '$'),
            ],
        },
        fallbacks=[CommandHandler('stop', stop)],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
