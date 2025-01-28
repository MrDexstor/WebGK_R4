from telegram.ext import ContextTypes, CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from TelegramBot.datamitrix.matrixGenerator import generateDataMatrix

async def cmd_gdm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    args = context.args
    if len(args) < 1:
        await update.message.reply_text('Недостаточно аргументов. Использование: /gdm <barcode> {count_dm:optional}')
        return

    #Получаем штрих из запроса
    barcode = args[0]

    #Получаем кол-во матриксов
    if len(args) == 2:
        dm_count = int(args[1])
    else:
        dm_count = 1

    #Ограничиваем колво матриксов за раз
    if dm_count > 9:
        dm_count = 9

    matrix_code = generateDataMatrix(barcode, dm_count)
    await update.message.reply_media_group(media=matrix_code, caption=f'DataMatrix для товара {barcode}\nGTIN:{barcode}')
    keyboard = [
        [InlineKeyboardButton("Остаток товара в программе не соответствует действительному", callback_data='mismatch_stock')],
        [InlineKeyboardButton("Остаток 0", callback_data='zero_stock')],
        [InlineKeyboardButton("Товар в текущем приходе", callback_data='current_arrival')],
        [InlineKeyboardButton("Нет времени искать товар", callback_data='no_time')],
        [InlineKeyboardButton("DM не читается/отсувствует", callback_data='dm_issue')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.sendMessage(chat_id=update.effective_chat.id, text='Для улучшение сервиса, просим вам выбрать причину по которой вы запросили DataMatrix. Выберите клавишу соответствующую вашей причине', reply_markup=reply_markup)


def response_reacon(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    button_data = query.data
    chat_id = query.message.chat_id