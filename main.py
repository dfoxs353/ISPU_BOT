import telegram
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters


# список новостей
news = [
    {
        'title': 'Новость 1',
        'photo_url': 'https://sun9-57.userapi.com/impg/50LomoU5g9lvbVjJJ7dgJ9AcnvSNVl62sGdXFg/Q1IvnNr4WVE.jpg?size=886x591&quality=96&sign=1994287f8155527e31b4e304aac92f12&type=album',
        'text': 'PowerQ объявляем старт набора на одиннадцатую Школу Кураторов ИГЭУ Территория Q - 2023, которая пройдёт в августе на Рубском озере! Ты хочешь стать куратором? Делиться своим опытом? Тогда не упусти уникальную возможность получить много ярких эмоций, развить в себе новые навыки, реализовать свои интересные идеи и завести новых друзей…'
    },
    {
        'title': 'Новость 2',
        'photo_url': 'https://sun9-4.userapi.com/impg/cAO8A3PNcceex3VSPt2I6F0eL-aj8IhG_HlLqw/98Nc_ObbcNM.jpg?size=886x665&quality=96&sign=574c61ec7c459b5c279e792eb89e357f&type=album',
        'text': 'Команда из ИГЭУ заняла 1 место в Международной олимпиаде студентов по Электромеханике. С 25 по 27 апреля команда Электромеханического факультета принимала участие в Международной олимпиаде студентов по Электромеханике, проходившей в Уфимском университете науки и техники.'
    },
    {
        'title': 'Новость 3',
        'photo_url': 'https://sun1-85.userapi.com/impg/SkaP1ptxoktrqzhy4QtQUUnuEZ3ab8vXz4H6yQ/TBlJFAWrA8I.jpg?size=886x664&quality=96&sign=b2a69e5a80c68f8f4cfc9bbe87e28ab8&type=album',
        'text': 'Мужская и женская сборные ИГЭУ - серебряные призеры первомайской эстафеты «Рабочий край». Легкоатлеты ИГЭУ достойно представили свой ВУЗ и среди учебных заведений высшего образования заняли почётное 2 место.'
    }
]

# функция, которая будет вызываться при команде /start
def start(update, context):
    keyboard = [
        [ 'Посмотреть карту ВУЗа', 'Узнать новости ВУЗа', 'Информация о факультетах']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text('Выберите кнопку:', reply_markup=reply_markup)

# функция, которая будет вызываться при нажатии кнопки
def button_click(update, context):
    text = update.message.text
    if text == 'Посмотреть карту ВУЗа':
        post(update,context=context,url="http://ispu.ru/files/imagecache/640x480/cck-images/Korpusa_na_plane.jpg",text="Карта вуза")
    elif text == 'Узнать новости ВУЗа':
        
        for new in news:
            post(update,context=context,url=new['photo_url'],text=new['text'])
    elif text == 'Информация о факультетах':
        

        
        keyboard = [
            [ 'ИВТФ', 'ТЭФ', 'ЭЭФ']
            
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        update.message.reply_text('Выберите факультет:', reply_markup=reply_markup)
    elif text == 'ИВТФ': 
        post(update,context=context,url="http://ispu.ru/files/imagecache/640x480/cck-images/Korpusa_na_plane.jpg",text="ЕгороваКрутая")  
        keyboard = [
            [ 'Посмотреть карту ВУЗа', 'Узнать новости ВУЗа', 'Информация о факультетах']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        update.message.reply_text('Выберите кнопку:', reply_markup=reply_markup)


# функция, которая будет вызываться при отправке любого сообщения
def echo(update, context):
    update.message.reply_text('Я не понимаю команду. Выберите кнопку.')

def post(update, context,url,text):
    photo_text = text
    photo_url = url  
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url, caption=photo_text)


# функция, которая будет вызываться при команде /add_news
def add_news_start(update, context):
    update.message.reply_text('Введите заголовок новости:')
    return 1

# функция, которая будет вызываться при получении текстового сообщения в процессе добавления новости
def add_news_text(update, context):
    context.user_data['title'] = update.message.text
    update.message.reply_text('Отправьте картинку новости:')
    return 2

# функция, которая будет вызываться при получении картинки в процессе добавления новости
def add_news_photo(update, context):
    photo_file = update.message.photo[-1].get_file()
    context.user_data['photo'] = photo_file.file_path
    update.message.reply_text('Введите текст новости:')
    return 3

# функция, которая будет вызываться при получении текстового сообщения после отправки картинки
def add_news_finish(update, context):
    title = context.user_data.get('title')
    photo_url = context.user_data.get('photo')
    text = update.message.text
    
    news_item = {
        'title': title,
        'photo_url': photo_url,
        'text': text
    }
    news.append(news_item)

    update.message.reply_text('Новость добавлена успешно!')

    
TOKEN = '6175253959:AAFnzsItYpZrVCoK-DtQaZ81OnAgJM-lxmY'


bot = telegram.Bot(token=TOKEN)


updater = Updater(bot=bot)


updater.dispatcher.add_handler(CommandHandler('start', start))

updater.dispatcher.add_handler(MessageHandler(Filters.text, button_click))


#updater.dispatcher.add_handler(CommandHandler('add_news', add_news_start))
#updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), add_news_text))
#updater.dispatcher.add_handler(MessageHandler(Filters.photo, add_news_photo))
#updater.dispatcher.add_handler(CommandHandler('cancel', add_news_finish, pass_args=True))




updater.dispatcher.add_handler(MessageHandler(Filters.all, echo))


updater.start_polling()

