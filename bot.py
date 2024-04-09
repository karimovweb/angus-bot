import telebot  
import database
import buttons
import logging
import threading
import time

from telebot import types
logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot("6986619740:AAFJvNoqZGZZ55C7vlkREEq9wWCQ5Rpll4Y")
users = {}
print(database.get_users())


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if database.check_users(user_id):
        if database.check_language(user_id) == 'uzb':
            main_menu_uz(message)

        else:
            main_menu(message)
            print(database.get_user_name(user_id))
    else:
        bot.send_message(user_id, "Выберите язык/Tilni tanlang:", reply_markup=buttons.language_kb())
        bot.register_next_step_handler(message, registration)

def registration(message):
    user_id = message.from_user.id
    if message.text == "Русский язык 🇷🇺":
        language = "Rus"
        bot.send_message(user_id, "Напишите своё Имя Фамилию: ")
        bot.register_next_step_handler(message, get_name, language)
    elif message.text == "O'zbek tili 🇺🇿":
        language = "Uzb"
        bot.send_message(user_id, "Ismingizni kiriting: ")
        bot.register_next_step_handler(message, get_name_uz, language)
        # database.add_user(user_id, "uzb")
    else:
        bot.send_message(user_id, "Выберите язык из списка в меню / Tilni menudan tanlang",
                         reply_markup=buttons.language_kb())
        bot.register_next_step_handler(message, registration)

def get_name(message, language):
    user_id = message.from_user.id
    name = message.text
    users[user_id] = [name, language]
    bot.send_message(user_id, "Место работы: ", reply_markup=buttons.work_kb())
def get_name_uz(message, language):
    user_id = message.from_user.id
    name = message.text
    users[user_id] = [name, language]
    bot.send_message(user_id, "Ish joyingizni kiriting: ", reply_markup=buttons.work_kb_uz())

def choosing_payment(message):
    user_id = message.from_user.id
    lend = [message.text]
    users[user_id] = lend
    print(users)
    bot.send_message(user_id, "Через какую платформу хотите заплатить?", reply_markup=buttons.payment())
def choosing_payment_uz(message):
    user_id = message.from_user.id
    lend = [message.text]
    users[user_id] = lend
    print(users)
    bot.send_message(user_id, "Qaysi platforma orqali pul to'lamoxchisiz?", reply_markup=buttons.payment_uz())

@bot.callback_query_handler(lambda call: call.data in ['Чирчик', 'ВВС Управление', 'Академия Вооруженных Сил', 'Центральный военный госпиталь',
                                                       'Chirchiq', 'Markaziy harbiy kasalxona', 'XHK Boshqarmasi', 'Qurolli Kuchlar Akademiyas'])
def get_work(call):
    user_id = call.message.chat.id
    work = call.data
    if users.get(user_id)[1] == "Rus":
        bot.send_message(user_id, "Отправьте свой номер телефона: ", reply_markup=buttons.get_phone_number())
        bot.register_next_step_handler(call.message, get_number, work)
    elif users.get(user_id)[1] == "Uzb":
        bot.send_message(user_id, "Telefon raqamingizni jo'nating: ", reply_markup=buttons.get_phone_number_uz())
        bot.register_next_step_handler(call.message, get_number_uz, work)
def get_number(message, work):
    user_id = message.from_user.id
    if user_id in users:
        if message.contact:
            phone_number = message.contact.phone_number
            bot.send_message(user_id, "Вы успешно зарегестрировались!", reply_markup=types.ReplyKeyboardRemove())
            database.add_user(user_id, users.get(user_id)[0], work, phone_number, users.get(user_id)[1])
            bot.send_message(-1001996929800, f"Новый курьер: \n"
                                             f"Имя: {users.get(user_id)[0]} \n"
                                             f"Локация: {work} \n"
                                             f"Контактный номер: {phone_number} \n"
                                             f"Аккаунт: @{message.from_user.username}" , reply_markup=types.ReplyKeyboardRemove())
            users.pop(user_id)
            print(database.get_user_name(user_id))
            bot.send_photo(user_id, photo=open('photo_2024-02-20_23-47-23.jpg', 'rb'),
                           caption=f'Здравствуйте, дорогой {database.get_user_name(user_id)}! \n'
                                   f'Добро пожаловать в мясной интернет-магазин "Angus"! \n'
                                   f'Используйте нужные вам разделы:',
                           reply_markup=buttons.pay_feedback())
            print(database.get_users())
        else:
            bot.send_message(user_id, "Ошибка! Перезагрузите бота")
    else:
        bot.send_message(user_id, "Отправьте свой номер через кнопку")
        bot.register_next_step_handler(message, get_number, work)
def get_number_uz(message, work):
    user_id = message.from_user.id
    if user_id in users:
        if message.contact:
            phone_number = message.contact.phone_number
            bot.send_message(user_id, "Siz muvaffaqiyatli ro'yxatdan o'tdingiz!", reply_markup=types.ReplyKeyboardRemove())
            database.add_user(user_id, users.get(user_id)[0], work, phone_number, users.get(user_id)[1])
            bot.send_message(-1001996929800, f"Yangi kuryer: \n"
                                             f"Ismi: {users.get(user_id)[0]} \n"
                                             f"Lokatsiya: {work} \n"
                                             f"Telefon raqam: {phone_number} \n"
                                             f"Akkaunt: @{message.from_user.username}", reply_markup=types.ReplyKeyboardRemove())
            users.pop(user_id)
            database.get_users()
            bot.send_photo(user_id, photo=open('photo_2024-02-20_23-47-23.jpg', 'rb'),
                           caption=f"Assalomu aleykum, xurmatli {database.get_user_name(user_id)}! \n"
                                   f"'Angus' Onlayn Go'sht do'koniga xush kelibsiz! \n"
                                   f"Sizga kerak bo'lgan bo'limlardan foydalaning:",
                           reply_markup=buttons.pay_feedback_uz())
            print(users)
        else:
            bot.send_message(user_id, "Xatolik! Qayta urinib ko'ring")
    else:
        bot.send_message(user_id, "Telefon raqamingizni jo'nating")
        bot.register_next_step_handler(message, get_number, work)

@bot.callback_query_handler(lambda call: call.data in ['pay', 'feedback', 'click', 'payme', 'paynet', 'zaplatil', 'otmenit', 'skinul',
                                                       'pay_uz', 'feedback_uz', 'click_uz', 'payme_uz', 'paynet_uz', 'zaplatil_uz',
                                                       'otmena', 'tashladim', 'toladim', 'back', 'main_menu', 'orqaga', 'mailing', 'send_message'])
def pay_answer(call):
    user_id = call.message.chat.id
    if call.data == 'pay':
        bot.send_message(user_id, "Введите сумму которую заплатите:\n"
                                  "В виде: 100.000 сум", reply_markup=buttons.back())
        bot.register_next_step_handler(call.message, choosing_payment)
    elif call.data == 'feedback':
        bot.send_message(user_id, "Оставьте свой отзыв или письмо админу: ", reply_markup=buttons.back())
        if call.message:
            bot.register_next_step_handler(call.message, feedback_fc)

    elif call.data == 'click':
        bot.send_message(user_id, f'''
        Ваше имя: {database.get_user_name(user_id)[0]};
Скиньте сумму {users.get(user_id)[0]} в этот кошелёк:
8600332986772477
Норбобоева Лилия''', reply_markup=buttons.oplata_otmen())
    elif call.data == 'payme':
        bot.send_message(user_id, f'''Ваше имя: {database.get_user_name(user_id)};
Скиньте сумму {users.get(user_id)[0]} в этот кошелёк:
8600332986772477
Норбобоева Лилия''', reply_markup=buttons.oplata_otmen())
    elif call.data == 'paynet':
        bot.send_message(user_id, f'''Ваше имя: {database.get_user_name(user_id)};
Скиньте сумму {users.get(user_id)[0]} в этот кошелёк:
8600332986772477
Норбобоева Лилия''', reply_markup=buttons.oplata_otmen())
    elif call.data == 'zaplatil':
        bot.send_message(user_id, "Скиньте чек оплаты сюда: @adminangus 🟢", reply_markup=buttons.oplata())
    elif call.data == 'otmenit':
        bot.send_photo(user_id, photo=open('photo_2024-02-20_23-47-23.jpg', 'rb'),
                       caption=f'Здравствуйте, дорогой {database.get_user_name(user_id)}! \n'
                               f'Добро пожаловать в мясной интернет-магазин "Angus"!\n'
                               f'Используйте нужные вам разделы:',
                       reply_markup=buttons.pay_feedback())
        # bot.register_next_step_handler(call.data, feedback_fc)
    elif call.data == 'skinul':
        bot.send_message(user_id, "Спасибо за платёж! Наши админы скоро просмотрят и зачеркнут ваш долг ✅")
        bot.send_photo(user_id, photo=open('photo_2024-02-20_23-47-23.jpg', 'rb'),
                       caption=f'Здравствуйте, дорогой {database.get_user_name(user_id)}! \n'
                            f'Добро пожаловать в мясной интернет-магазин "Angus"! \n'
                            f'Используйте нужные вам разделы:',
                       reply_markup=buttons.pay_feedback())
        bot.send_message(-1001996929800, f'''<b> Заплата за долг:</b> {users.get(user_id)[0]} сум
        
<b>Имя:</b> {database.get_user_name(user_id)}

<b>Телефонный номер:</b> {database.get_number(user_id)}

<b>Район:</b> {database.get_location(user_id)[0]}

<b>ID аккаунта:</b> {database.check_id(user_id)[0]}''',
                         parse_mode='HTML')
    elif call.data == 'pay_uz':
        bot.send_message(user_id, "Siz to'laydigan miqdorni kiriting::\n"
                                  "Shakli: 100.000 so'm", reply_markup=buttons.back_uz())
        bot.register_next_step_handler(call.message, choosing_payment_uz)
    elif call.data == 'feedback_uz':
        bot.send_message(user_id, "O'z izohinggizni qoldirishinggiz mumkun: ", reply_markup=buttons.back_uz())
        if call.message:
            bot.register_next_step_handler(call.message, feedback_fc_uz)
    elif call.data == 'click_uz':
        bot.send_message(user_id, f'''
        Ismingiz: {database.get_user_name(user_id)}
{users.get(user_id)[0]} miqdorni ushbu hamyonga o'tkazing:
8600332986772477
Норбобоева Лилия''', reply_markup=buttons.oplata_otmen_uz())
    elif call.data == 'payme_uz':
        bot.send_message(user_id, f'''Ismingiz: {database.get_user_name(user_id)}
{users.get(user_id)[0]} miqdorni ushbu hamyonga o'tkazing:
8600332986772477
Норбобоева Лилия''', reply_markup=buttons.oplata_otmen_uz())
    elif call.data == 'paynet_uz':
        bot.send_message(user_id, f'''Ismingiz: {database.get_user_name(user_id)}
{users.get(user_id)[0]} miqdorni ushbu hamyonga o'tkazing:
8600332986772477
Норбобоева Лилия''', reply_markup=buttons.oplata_otmen_uz())
    elif call.data == 'toladim':
        bot.send_message(user_id, text="To'lov chekini ushbu adminga yuboring: @adminangus 🟢",
                         reply_markup=buttons.oplata_uz())
    elif call.data == 'otmena':
        bot.send_photo(user_id, photo=open('photo_2024-02-20_23-47-23.jpg', 'rb'),
                       caption=f"Assalomu aleykum, xurmatli {database.get_user_name(user_id)}! \n"
                               f"'Angus' Onlayn go'sht do'koniga xush kelibsiz! \n"
                               f"Sizga kerak bo'lgan bo'limlardan foydalaning:",
                       reply_markup=buttons.pay_feedback_uz())
        # bot.register_next_step_handler(call.data, feedback_fc)
    elif call.data == 'tashladim':
        bot.send_message(user_id, "To'lov uchun rahmat! Adminlarimiz tez orada ko'rib chiqishadi va qarzingizni o'chirib tashlashadi ✅")
        bot.send_photo(user_id, photo=open('photo_2024-02-20_23-47-23.jpg', 'rb'),
                       caption=f"Assalomu aleykum, xurmatli {database.get_user_name(user_id)}! \n"
                               f"'Angus' Onlayn Go'sht do'koniga xush kelibsiz! \n"
                               f"Sizga kerak bo'lgan bo'limlardan foydalaning:",
                       reply_markup=buttons.pay_feedback_uz())
        bot.send_message(-1001996929800, f'''<b>Заплата за долг:</b> {users.get(user_id)[0]} сум
        
<b>Имя:</b> {database.get_user_name(user_id)}

<b>Телефонный номер:</b> {database.get_number(user_id)}

<b>Район:</b> {database.get_location(user_id)[0]}

<b>ID аккаунта:</b> {database.check_id(user_id)[0]}''',
                         parse_mode='HTML')
    elif call.data =='back':
        bot.send_photo(user_id, photo=open('photo_2024-02-20_23-47-23.jpg', 'rb'),
                           caption=f'Здравствуйте, дорогой {database.get_user_name(user_id)}! \n'
                                   f'Добро пожаловать в мясной интернет-магазин "Angus"! \n'
                                   f'Используйте нужные вам разделы:', reply_markup=buttons.pay_feedback())
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    elif call.data == 'orqaga':
        bot.send_photo(user_id, photo=open('photo_2024-02-20_23-47-23.jpg', 'rb'),
                       caption=f"Assalomu aleykum, xurmatli {database.get_user_name(user_id)}! \n"
                               f"'Angus' Onlayn Go'sht do'koniga xush kelibsiz! \n"
                               f"Sizga kerak bo'lgan bo'limlardan foydalaning:", reply_markup=buttons.pay_feedback_uz())
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    elif call.data == "mailing":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id,
                         "Введите текст рассылки или отправьте фотографию с описанием, либо отмените рассылку через кнопку в меню",
                         reply_markup=buttons.canceling())
        bot.register_next_step_handler(call.message, mailing_to_all)
    elif call.data == "send_message":
        bot.delete_message(user_id, call.message.message_id)
        bot.send_message(user_id, "Введите айди пользователя, которому вы хотите написать",
                         reply_markup=buttons.canceling())
        bot.register_next_step_handler(call.message, send_answer)


def feedback_fc(message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    print(database.get_number(user_id))
    bot.send_message(-1001996929800, f" Отзыв: {message.text}\n \n \n"
                                     f"Username пользователя: @{user_name}\n \n \n"
                                     f"Телефон номер: {database.get_number(user_id)}")
    bot.send_photo(user_id, photo=open('photo_2024-02-20_23-47-23.jpg', 'rb'), caption=f'Здравствуйте, дорогой {database.get_user_name(user_id)}! \n'
                                                                                       f'Добро пожаловать в мясной интернет-магазин "Angus"! \n'
                                                                                       f'Используйте нужные вам разделы:',
                   reply_markup=buttons.pay_feedback())
def feedback_fc_uz(message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    print(database.get_number(user_id))
    bot.send_message(-1001996929800, f" Отзыв: {message.text}\n \n \n"
                                     f"Username пользователя: @{user_name}\n \n \n"
                                     f"Телефон номер: {database.get_number(user_id)}")
    bot.send_photo(user_id, photo=open('photo_2024-02-20_23-47-23.jpg', 'rb'), caption=f"Assalomu aleykum, xurmatli {database.get_user_name(user_id)}! \n"
                                                                                       f"'Angus' Onlayn Go'sht do'koniga xush kelibsiz! \n"
                                                                                       f"Sizga kerak bo'lgan bo'limlardan foydalaning:",
                   reply_markup=buttons.pay_feedback_uz())

def main_menu(message):
    user_id = message.from_user.id
    bot.send_photo(user_id, photo=open('photo_2024-02-20_23-47-23.jpg', 'rb'), caption=f'Здравствуйте, дорогой {database.get_user_name(user_id)}! \n'
                                                                                       f'Добро пожаловать в мясной интернет-магазин "Angus"! \n'
                                                                                       f'Используйте нужные вам разделы:',
                   reply_markup=buttons.pay_feedback())
def main_menu_uz(message):
    user_id = message.from_user.id
    bot.send_photo(user_id, photo=open('photo_2024-02-20_23-47-23.jpg', 'rb'), caption=f"Assalomu aleykum, xurmatli {database.get_user_name(user_id)}! \n"
                                                                                       f"'Angus' Onlayn Go'sht do'koniga xush kelibsiz! \n"
                                                                                       f"Sizga kerak bo'lgan bo'limlardan foydalaning:",
                   reply_markup=buttons.pay_feedback_uz())
@bot.message_handler(commands=["admin"])
def admin_panel(message):
    user_id = message.from_user.id
    types.ReplyKeyboardRemove()
    if user_id == 1532198392 or user_id == 5692665577:
        bot.send_message(user_id, "Админ панель. Выберите действие",
                         reply_markup=buttons.main_admin_menu())
    else:
        pass
def send_message_to_user(target_id, text, photo):
    target = target_id[0]
    if photo == None:
        try:
            time.sleep(0.2)
            bot.send_message(target, text)
        except:
            pass
    else:
        try:
            time.sleep(0.2)
            bot.send_photo(target_id, photo=photo, caption=text)
        except:
            pass
def mailing_to_all(message):
    user_id = message.from_user.id
    targets_id = database.mailing_all()
    if message.text == "Отмена❌":
        bot.send_message(user_id, "Рассылка отменена", reply_markup=types.ReplyKeyboardRemove())
    elif message.photo:
        photo = message.photo[-1].file_id
        text = message.caption
        for target_id in targets_id:
            thread = threading.Thread(target=send_message_to_user, args=(target_id, text, photo))
            thread.start()
    else:
        for target_id in targets_id:
            text = message.text
            photo = None
            thread = threading.Thread(target=send_message_to_user, args=(target_id, text, photo))
            thread.start()
    bot.send_message(user_id, "Рассылка завершена", reply_markup=types.ReplyKeyboardRemove())
def send_answer(message):
    admin_id = message.from_user.id
    if message.text == "Отмена❌":
        bot.send_message(admin_id, "Действие отменено", reply_markup=types.ReplyKeyboardRemove())
    else:
        try:
            user_id = int(message.text)
            bot.send_message(admin_id, "Введите сообщения для пользователя", reply_markup=buttons.canceling())
            bot.register_next_step_handler(message, send_full_answer, user_id)
        except:
            bot.send_message(admin_id, "Неправильный айди", reply_markup=types.ReplyKeyboardRemove())
def send_full_answer(message, user_id):
    admin_id = message.from_user.id
    if message.text == "Отмена❌":
        bot.send_message(admin_id, "Действие отменено", reply_markup=types.ReplyKeyboardRemove())
    elif message.photo:
        photo = message.photo[-1].file_id
        bot.send_photo(user_id, photo=photo, caption=message.caption)
        bot.send_message(admin_id, "Ответ отправлен", reply_markup=types.ReplyKeyboardRemove())
    else:
        text = message.text
        try:
            bot.send_message(user_id, text)
            bot.send_message(admin_id, "Ответ отправлен", reply_markup=types.ReplyKeyboardRemove())
        except:
            bot.send_message(admin_id, "Не удалось отправить ответ", reply_markup=types.ReplyKeyboardRemove())

bot.infinity_polling()