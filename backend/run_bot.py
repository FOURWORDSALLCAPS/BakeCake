import logging

from django.utils import timezone
from environs import Env
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update, MessageEntity, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    CallbackContext,
    MessageHandler,
    Filters
)

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

import django
django.setup()

from core.models import AboutUs, Cake
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

END = ConversationHandler.END

CUSTOMIZATION, STANDARD_CAKE, ABOUT_US, SELECTING_ACTION = map(chr, range(4))

START_OVER, SHOWING, STOPPING, CUSTOM_CAKE = map(chr, range(4, 8))

TOPPING, BERRIES, DECOR, INSCRIPTION, COMMENT, QUANTITY_LEVEL, FORM, BACK, CAKE_ID, USER_CAKE, DONE = map(chr, range(8, 19))

CAKE = {}


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

    cakes = Cake.objects.all()

    for cake in cakes:
        bold_entity = MessageEntity(
            type=MessageEntity.BOLD, offset=0, length=len(cake.name)
        )
        buttons = [
            [
                InlineKeyboardButton(
                    text='Выбрать', callback_data=str(CAKE_ID)
                ),
            ],
        ]
        keyboard = InlineKeyboardMarkup(buttons)
        update.callback_query.message.reply_photo(
            cake.image,
            cake.name + '\n\n' + f'{str(cake.price)}р',
            caption_entities=[bold_entity],
            reply_markup=keyboard,
        )

    return STANDARD_CAKE


def about_us(update: Update, context: CallbackContext) -> str:
    """Handle the selection of cake topping."""

    information_about_us = AboutUs.objects.first()

    text = (
        f"Ссылка на Telegram: {information_about_us.telegram}\n"
        f"Ссылка на Instagram: {information_about_us.instagram}\n"
        f"Номер телефона: {information_about_us.phone_number}\n"
        f"Адрес: {information_about_us.address}"
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
    query = update.callback_query
    quantity_levels = query.data.split('\r')
    CAKE['quantity_levels'] = quantity_levels[0]
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
    query = update.callback_query
    form = query.data.split('\x0e')
    CAKE['form'] = form[0]
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
    query = update.callback_query
    topping = query.data.split('\x08')
    CAKE['topping'] = topping[0]
    buttons = [
        [
            InlineKeyboardButton(text='Без топпинга', callback_data='Without'),
            InlineKeyboardButton(text='Белый соус', callback_data='white'),
            InlineKeyboardButton(text='Карамельный сироп', callback_data='Caramel'),
            InlineKeyboardButton(text='Кленовый сироп', callback_data='Maple'),
        ],
        [
            InlineKeyboardButton(text='Клубничный сироп', callback_data='Strawberry'),
            InlineKeyboardButton(text='Черничный сироп', callback_data='Blueberry'),
            InlineKeyboardButton(text='Молочный шоколад', callback_data='Milk'),
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
    query = update.callback_query
    berries = query.data.split('\t')
    CAKE['berries'] = berries[0]
    buttons = [
        [
            InlineKeyboardButton(text='Ежевика', callback_data='Blackberry'),
            InlineKeyboardButton(text='Малина', callback_data='Raspberry'),
            InlineKeyboardButton(text='Голубика', callback_data='Blueberries'),
            InlineKeyboardButton(text='Клубника', callback_data='Strawberry'),
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
    query = update.callback_query
    decor = query.data.split('\n')
    CAKE['decor'] = decor[0]
    buttons = [
        [
            InlineKeyboardButton(text='Фисташки', callback_data='Pistachios'),
            InlineKeyboardButton(text='Безе', callback_data='Meringue'),
            InlineKeyboardButton(text='Фундук', callback_data='Hazelnut'),
        ],
        [
            InlineKeyboardButton(text='Пекан', callback_data='Pecan'),
            InlineKeyboardButton(text='Маршмеллоу', callback_data='marshmallow'),
            InlineKeyboardButton(text='Марципан', callback_data='Marzipan'),
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data=str(END)),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    context.user_data[START_OVER] = False

    return CUSTOM_CAKE


def handle_inscription_selection(update: Update, context: CallbackContext) -> str:
    """Handle the selection of cake topping."""
    text = "Введите текст надписи для торта:"
    query = update.callback_query
    inscription = query.data.split('\x0e')
    CAKE['inscription'] = inscription[0]
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)

    context.user_data[START_OVER] = False

    return CUSTOM_CAKE


def handle_comment_selection(update: Update, context: CallbackContext) -> str:
    """Handle the selection of cake topping."""
    text = "Введите текст с комментарием к торту:"
    query = update.callback_query
    comment = query.data.split('\x0e')
    CAKE['comment'] = comment[0]
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
    print(CAKE)
    return CUSTOM_CAKE


def handle_cake_address_selection(update: Update, context: CallbackContext) -> str:
    query = update.callback_query
    delivery_address = query.data.split('\n')
    CAKE['delivery_address'] = delivery_address[0]

    query.message.reply_text(
        'Введите адрес доставки:',
        reply_markup=ReplyKeyboardRemove(),
    )

    context.user_data[START_OVER] = False

    return CUSTOM_CAKE


def assemble_cake():
    create_user_cake(price=CAKE[''], comment=CAKE[''], form=CAKE[''], quantity_levels=CAKE[''],
                     topping=CAKE[''], inscription=CAKE[''], delivery_address=CAKE[''], delivery_date=timezone.now())


def create_user_cake(price, comment, form, quantity_levels,
                     topping, inscription, delivery_address, delivery_date):
    cake = Cake(
        price=price,
        comment=comment,
        form=form,
        quantity_levels=quantity_levels,
        topping=topping,
        inscription=inscription,
        delivery_address=delivery_address,
        delivery_date=delivery_date,
    )
    cake.save()


def enter_address(update: Update, context: CallbackContext) -> int:
    user_address = update.message.text

    CAKE['delivery_address'] = user_address

    buttons = [
        [
            InlineKeyboardButton(text='Согласится с обработкой персональных данных', callback_data=str(USER_CAKE)),
        ],
        [
            InlineKeyboardButton(text='ОТКАЗАТСЯ от обработки персональных данных', callback_data=str(DONE)),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    update.message.reply_text(
        f'Вы ввели адрес доставки: {user_address}\n'
        'Спасибо за то, что выбираете нас!',
        reply_markup=keyboard
    )

    return STANDARD_CAKE


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
                CallbackQueryHandler(stop, pattern='^' + str(DONE) + '$'),
                MessageHandler(Filters.text, enter_address)
            ],
            STANDARD_CAKE: [
                CallbackQueryHandler(end_second_level, pattern='^' + str(END) + '$'),
                CallbackQueryHandler(stop, pattern='^' + str(STOPPING) + '$'),
                CallbackQueryHandler(handle_showing_selection, pattern='^' + str(SHOWING) + '$'),
                CallbackQueryHandler(handle_cake_address_selection, pattern='^' + str(CAKE_ID) + '$'),
            ],
            ABOUT_US: [
                CallbackQueryHandler(end_second_level, pattern='^' + str(END) + '$'),
            ],
        },
        fallbacks=[CommandHandler('stop', stop)],
    )
    dispatcher.add_handler(CallbackQueryHandler(handle_quantity_level_selection, pattern='^(1|2|3)$'))
    dispatcher.add_handler(CallbackQueryHandler(handle_cake_form_selection, pattern='^(round|rectangular|square)$'))
    dispatcher.add_handler(CallbackQueryHandler(handle_decor_selection, pattern='^(Pistachios|Meringue|Hazelnut|Pecan|Marshmallow|Marzipan)$'))
    dispatcher.add_handler(CallbackQueryHandler(handle_berries_selection, pattern='^(Blackberry|Raspberry|Blueberries|Strawberry)$'))
    dispatcher.add_handler(CallbackQueryHandler(handle_topping_selection, pattern='^(Without|White|Caramel|Maple|Strawberry|Blueberry|Milk)$'))
    dispatcher.add_handler(CallbackQueryHandler(handle_cake_address_selection, pattern='^(Delivery_address)$'))

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
