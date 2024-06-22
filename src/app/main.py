from datetime import datetime, timedelta
import threading
import time
import flask
from src.utils.spreadsheet import worksheet, worksheet_registration, worksheet_send
from configs.config import TOKEN, TOKEN_TEST, ADMIN_ID
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

bot = Bot(TOKEN)
dp = Dispatcher()

class TelegramBot():
    def __init__(self, TOKEN) -> None:
        pass

# app = flask.Flask(__name__)
bot.remove_webhook()



# Переменная для хранения информации о блокировке пользователей
blocked_users = {}

# Переменная для хранения времени последнего отправленного сообщения от каждого пользователя
last_message_time = {}

# Функция для проверки регистрации пользователя в таблице
def is_registered(user_id):
    try:
        user_id = str(user_id)
        users = worksheet_registration.col_values(2)  # Получаем столбец с идентификаторами пользователей
        return user_id in users
    except Exception as e:
        print(f"Error while checking registration: {e}")
        return False

        start_button(user_id)


# Функция для блокировки пользователя на некоторое время
def block_user(user_id, seconds):
    print("something")
    int(user_id)
    # Блокируем пользователя на указанное количество секунд
    blocked_users[user_id] = datetime.now() + timedelta(seconds=seconds)
    print(blocked_users)
    def unblock():
        blocked_users.pop(user_id, None)

    threading.Timer(seconds, unblock).start()



# Функция для проверки спама по количеству запросов за определенный период
def check_spam(user_id):
    current_time = datetime.now()
    last_messages = last_message_time.get(user_id, [])
    if not last_messages or (current_time - last_messages[-1]) >= timedelta(seconds=2):
        # Обновляем время последнего отправленного сообщения
        last_messages.append(current_time)
        last_message_time[user_id] = last_messages
        return True

    return False



# Функция для сохранения другого
def save_other(message, registred_row, current_col):
    try:
        answer = message.text.strip()
        worksheet.update_cell(registred_row, current_col, answer)  # Обновляем ответ в таблице
        get_question(message, current_col + 1, registred_row)  # Переходим к следующему вопросу
    except Exception as e:
        bot.send_message(message.from_user.id, 'Произошла ошибка. Пожалуйста, попробуйте еще раз.')
        print(f"Error while saving city: {e}")
        start_button(message.chat.id)

# Функция для сохранения другого
def save_ambassador(message, registred_row, current_col):
    try:
        answer = message.text.strip()
        worksheet.update_cell(registred_row, 94, answer)  # Обновляем ответ в таблице
        get_question(message, current_col + 1, registred_row)  # Переходим к следующему вопросу
    except Exception as e:
        bot.send_message(message.from_user.id, 'Произошла ошибка. Пожалуйста, попробуйте еще раз.')
        print(f"Error while saving city: {e}")
        start_button(message.chat.id)

# Функция для сохранения другого
def save_friends(message, registred_row, current_col):
    try:
        answer = message.text.strip()
        worksheet.update_cell(registred_row, 95, answer)  # Обновляем ответ в таблице
        get_question(message, current_col + 1, registred_row)  # Переходим к следующему вопросу
    except Exception as e:
        bot.send_message(message.from_user.id, 'Произошла ошибка. Пожалуйста, попробуйте еще раз.')
        print(f"Error while saving city: {e}")
        start_button(message.chat.id)


# Функция для получения вопроса из Google sheets
def get_question(message, current_col, registred_row):
    try:
        print(current_col)
        if current_col == 26:
            current_col += 1
        
        if current_col == 20:
            current_col += 1

        question = worksheet.cell(1, current_col).value
        coodinates = "split" + str(registred_row) + "split" + str(current_col)
        menu = telebot.types.InlineKeyboardMarkup()
        if current_col < 19:
            bot.send_message(message.chat.id, "🟣 Ты находишься на " + str(current_col-3) + " вопросе из 15.")

        if question == "Выбери секцию:":
            menu.add(telebot.types.InlineKeyboardButton(text = 'Хочу в IT', callback_data ='Хочу в IT' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Уже в IT', callback_data ='Уже в IT' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Биохим', callback_data ='Биохим' + coodinates))
            msg = bot.send_message(message.chat.id, "🟡 " + question + "\n\n👼 'Хочу в IT' - для тех, кто ещё ни разу не работал в сфере информационных технологий, но желает туда попасть\n\n🖥 'Уже в IT' - эта же секция предназначеная для ребят, кто уже работает и хочет повысить своей грейд на работе, но пока не знает как или у него не получается\n\n🧬 'Биохим' - секция предназначенная для двигателей инновация в медицине - биотехнологов и фармацевтов, а также для сферы энергетики и нефтегаза, которым трудно найти комьюнити или трудоустроиться из-за специфичности их сфер", reply_markup = menu)

        elif question == "В каком городе ты сейчас проживаешь?":
            menu.add(telebot.types.InlineKeyboardButton(text = 'Москва', callback_data ='Москва' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Московская область', callback_data ='Московская область' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Санкт-Петербург', callback_data ='Санкт-Петербург' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Казань', callback_data ='Казань' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Уфа', callback_data ='Уфа' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Белгород', callback_data ='Белгород' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Краснодар', callback_data ='Краснодар' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Нижний Новгород', callback_data ='Нижний Новгород' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Ростов-на-Дону', callback_data ='Ростов-на-Дону' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Другой', callback_data ='Другой' + coodinates))
            msg = bot.send_message(message.chat.id, text = "🟡 " + question, reply_markup = menu)

        elif question == "Информация для тех, кто не из Москвы!\n\nОбращаем внимание, что к сожалению, организаторы не могут покрыть твой проезд и проживание на форум. Однако мы можем помочь тебе оформить документы для покрытия поездки от ВУЗа.":
            menu.add(telebot.types.InlineKeyboardButton(text = 'Готов оплатить сам', callback_data ='Оплачу' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Не готов оплачивать сам', callback_data ='Не оплачу' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Попробую через вуз', callback_data ='Вуз' + coodinates))
            msg = bot.send_message(message.chat.id, text = "🟡 " + question, reply_markup = menu)

        elif question == "Из какого ты университета? Если ты закончил, то в каком учился?":
            menu.add(telebot.types.InlineKeyboardButton(text = 'МГУ', callback_data ='МГУ' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'ВШЭ', callback_data ='ВШЭ' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'МГТУ им. Баумана', callback_data ='МГТУ им. Баумана' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'МФТИ', callback_data ='МФТИ' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'МИФИ', callback_data ='МИФИ' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'МГМУ им. Сеченова', callback_data ='МГМУ им. Сеченова' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'РГУ им. Косыгина', callback_data ='РГУ им. Косыгина' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'РГУ НИУ им. Губкина', callback_data ='РГУ НИУ им. Губкина' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'МИСИС', callback_data ='МИСИС' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'МТУСИ', callback_data ='МТУСИ' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'РУДН', callback_data ='РУДН' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'РХТУ им. Менделеева', callback_data ='РХТУ им. Менделеева' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'МИРЭА', callback_data ='МИРЭА' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Другой', callback_data ='Другой' + coodinates))
            msg = bot.send_message(message.chat.id, text = "🟡 " + question, reply_markup = menu)

        elif question == "Подскажи свой курс:":
            menu.add(telebot.types.InlineKeyboardButton(text = '1-2 курс', callback_data ='1-2 курс' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = '3-5 курс', callback_data ='3-5 курс' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Магистратура', callback_data ='Магистратура' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Академ. отпуск', callback_data ='Академ. отпуск' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Выпустился/Работаю', callback_data ='Не учусь/работаю' + coodinates))
            msg = bot.send_message(message.chat.id, text = "🟡 " + question, reply_markup = menu)


        elif question == "Откуда узнал о нас?":
            menu.add(telebot.types.InlineKeyboardButton(text = 'Группа BreakPoint ВК', callback_data ='BreakPoint VK' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Запись в иной группе ВКонтакте', callback_data ='VK' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Увидел таргет-рекламу ВК', callback_data ='Target VK' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Instagram', callback_data ='Instagram' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'E-mail рассылка', callback_data ='E-mail' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Рассказали друзья', callback_data ='Друзья' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Увидел афишу на сайте', callback_data ='Афиша' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Публикация в Telegram канале', callback_data ='TG-каналы' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Состою в AIESEC', callback_data ='AIESEC' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Пришёл от амбассадора', callback_data ='Амбассадор' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Написал менеджер BreakPoint', callback_data ='От менеджера' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Другой', callback_data ='Другой' + coodinates))
            msg = bot.send_message(message.chat.id, text = "🟡 " + question + "\n\n- Запись в иной группе ВКонтакте - это группы университетов, паблики с мемами и прочее\n- Увидел афишу на сайте - это сайты университетов, сайты с мероприятиями", reply_markup = menu)

        elif question == "На каком основном языке программирования ты сейчас работаешь/учишься?":
            menu.add(telebot.types.InlineKeyboardButton(text = 'C++/C', callback_data ='C++/C' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Python', callback_data ='Python' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Java', callback_data ='Java' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'JavaScript', callback_data ='JavaScript' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'C#', callback_data ='C#' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'TypeScript', callback_data ='Университет' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'PHP', callback_data ='PHP' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Kotlin', callback_data ='Kotlin' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Swift', callback_data ='Swift' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Go', callback_data ='Go' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Scala', callback_data ='Scala' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Assambler', callback_data ='Assambler' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Другой', callback_data ='Другой' + coodinates))
            msg = bot.send_message(message.chat.id, text = "🟡 " + question, reply_markup = menu)

        elif question == "Хочешь ли ты участвовать в карьерной гостиной?":
            menu.add(telebot.types.InlineKeyboardButton(text = 'Да, хочу', callback_data ='Хочу' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Нет, не хочу', callback_data ='Не хочу' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Хочу, но резюме отправлю потом', callback_data ='Потом' + coodinates))
            msg = bot.send_message(message.chat.id, text = "🟡 " + question + "\n\nP.S. Карьерная Гостиная - это индивидуальная консультация с HR'ами топ компаний по твоему развитию. *Необходимо пройти отбор по CV/резюме", reply_markup = menu)
            
        elif question == "Хочешь ли ты стать амбассадором форума?":
            menu.add(telebot.types.InlineKeyboardButton(text = 'Да, это супер!', callback_data ='Амбассадорство' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Нет, откажусь', callback_data ='Отказ' + coodinates))
            msg = bot.send_message(message.chat.id, "🟡 " + question + "\n\n💁‍♂ Амбассадор - это человек, который представляет форум, с которым аудитория отождествляет что-то что-то большое, как, например, BreakPoint, и который доносит до них ценности инноваций и регистрации на наше событие!\n\n А лучшим амбассадорам мы вручим подарок: индивидуальное построение профессионального пути с карьерным консультантом!", reply_markup = menu)

        elif question == "Был ли ты в роли амбассадора раньше?":
            menu.add(telebot.types.InlineKeyboardButton(text = 'Да, был', callback_data ='Был' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Нет, это первый раз', callback_data ='Впервые' + coodinates))
            msg = bot.send_message(message.chat.id, text = "🟡 " + question, reply_markup = menu)

        elif question == "Я":
            menu.add(telebot.types.InlineKeyboardButton(text = 'Согласен на обработку данных', callback_data ='Согласен' + coodinates))
            msg = bot.send_message(message.chat.id, "🟡 " + question + " согласен на обработку моих персональных данных (https://drive.google.com/file/d/1D_iLWvFuqtWQN9PiExmQagBm83NmAJ4R/view?usp=sharing)\n\nСпасибо за регистрацию!😍\n\nДальше тебя ждёт стадия отбора, но, если ты заполнил всё подробно и искренне, то тебе не о чем переживать.\n\n🚀После этого нужно будет войти в чат, в который можно будет войти по ссылке из кнопки 'Статус регистрации', когда пройдёшь отбор - там будет вестись вся коммуникация между участниками, и, в конце концов, - приехать на форум 4 и 5 ноября!\n\nЖелаем удачи в прохождении отбора!", reply_markup = menu)
            worksheet.update_cell(registred_row, 87, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            worksheet_registration.update_cell(int(worksheet_registration.col_values(1)[len(worksheet_registration.col_values(1))-1])+1,2, message.chat.id)
            worksheet_registration.update_cell(int(worksheet_registration.col_values(1)[len(worksheet_registration.col_values(1))-1])+1,3, message.chat.username)
            worksheet_registration.update_cell(int(worksheet_registration.col_values(1)[len(worksheet_registration.col_values(1))-1])+2,1, int(worksheet_registration.col_values(1)[len(worksheet_registration.col_values(1))-1])+1)
                 
        elif question == "Сделал репост?🥺":
            menu.add(telebot.types.InlineKeyboardButton(text = 'Да!', callback_data ='Да!' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Нет', callback_data ='Не-а' + coodinates))
            msg = bot.send_message(message.chat.id, text = "🟡 " + question + '\n\nСделай репост записи https://vk.com/wall-48627112_14724, чтобы больше человек узнало о форуме!', reply_markup = menu)
                

        elif question == "Участвуешь в акции?":
            menu.add(telebot.types.InlineKeyboardButton(text = 'Да!', callback_data ='Да!' + coodinates))
            menu.add(telebot.types.InlineKeyboardButton(text = 'Нет', callback_data ='Не-а' + coodinates))
            msg = bot.send_message(message.chat.id, text = "🟡 " + question + '\n\nЕщё мы хотим тебе рассказать об акции: среди тех, кто приведёт 2-х или более друзей, мы разыграем заграничную стажировку Global Talant/Teaching (дальше GT), подробнее о которой ты узнаешь - https://aiesec.ru/!\n\nGT - это международные стажировки в разных странах, которые предлагаются AIESEC для развития лидерства и профессиональных навыках в сферах: IT, Sales, Marketing, Teaching и другие возможности\n\nP. S. Если вы приводите друга и хотите поучаствовать в розыгрыше, то пускай он при ответе на вопрос "Откуда узнал?" выберет "Узнал от друзей" и ввёт ваш ID - ' + str(registred_row), reply_markup = menu)
                

        else:
            if not question:
                invite = '''
Ссылка в чат участников: https://t.me/+0o0QVL0Cx1hjMTVi

Необходимо вступить в него, тк 
1.там будет публиковаться вся важная информация о форуме
2.также можно задать любые вопросы
3.познакомиться с другими участниками и найти коммьюнити — сможешь найти с кем пойти на форум

🟣 необходимо прочитать правила чата в закрепе чата
🟣 необходимо представиться в любом удобном формате

P.S. Если ты забудешь добавить в чат, наши менеджеры сами тебя добавят в него, чтобы ты не пропустил важную информацию и попал на форум🙂
                '''
                # Если вопрос пустой, значит все вопросы обработаны, завершаем регистрацию
                id = worksheet_registration.col_values(2).index(str(message.chat.id))
                if worksheet_registration.acell("D" + str(id+1)).value == "Поздравляем, ты прошёл отбор!🥳" or worksheet_registration.acell("D" + str(id+1)).value == "Поздравляем, ты прошла отбор!🥳":
                    bot.send_message(message.chat.id, invite)

                bot.send_message(message.chat.id, invite)
                file = open('чек-лист CV.pdf', 'rb')
                bot.send_message(message.chat.id, text = "Твой небольшой подарочек!🫶")
                bot.send_document(message.chat.id, file)
                start_button(message.chat.id)
                return
            bot.send_message(message.chat.id,"🟡 " + question)
            bot.register_next_step_handler(message, get_answer, current_col, registred_row)
    except Exception as e:
        # Если произошла ошибка при получении вопроса, выводим сообщение об ошибке
        bot.send_message(message.chat.id, 'Произошла ошибка при получении вопроса. Пожалуйста, попробуйте еще раз.')
        print(f"Error while getting question11: {e}")

        start_button(message.chat.id)



# Функция для сохранения ответов
def get_answer(message, current_col, registred_row):
    try:
        answer = message.text.strip()
        # Проверяем, если пользователь уже начал регистрацию
        if current_col > 3:
            # Проверяем ввод запрещенных фраз
            if answer in ["Регистрация", "Статус регистрации", "Наши социальные сети!", "Проблемы, пожелания и фидбек", "/start"]:
                bot.send_message(message.chat.id, 'Произошла ошибка! Пожалуйста, введите другой текст.')
                # Запрашиваем новый ответ
                bot.send_message(message.chat.id, 'Пожалуйста, введите новый ответ:')
                bot.register_next_step_handler(message, get_answer, current_col, registred_row)
                return  # Прерываем обработку ответа
        worksheet.update_cell(registred_row, current_col, answer)
        get_question(message, current_col + 1, registred_row)

    except Exception as e:
        # Если произошла ошибка при сохранении ответа, выводим сообщение об ошибке
        bot.send_message(message.from_user.id, 'Произошла ошибка при сохранении ответа. Пожалуйста, попробуйте еще раз.')
        print(f"Error while saving answer: {e}")

        start_button(message.chat.id)




# Функция для сохранения ответов из callback
@bot.callback_query_handler(func=lambda call: True)
def callback_saver(call: telebot.types.CallbackQuery):
    try:
        if call.data in ["Буду","К сожалению, не смогу;(","Пока не знаю"]:
            answer = call.data
            user_id = call.message.chat.id
            id = worksheet_send.col_values(3).index(str(user_id))
            worksheet_send.update_cell(id+1, 47, str(answer))  # Update the answer in the worksheet
            start_button(user_id)

        elif call.data in ["Backend","Frontend","System&Business", "Product&Data", "Фармацевтика", "Биотехнологии", "Нефтегаз", "Уже в IT"]:
            answer = call.data
            user_id = call.message.chat.id
            id = worksheet_send.col_values(3).index(str(user_id))
            worksheet_send.update_cell(id+1, 45+2, str(answer))  # Update the answer in the worksheet
            start_button(user_id)
            bot.send_message(user_id,"Спасибо за ответ!")

        else:
            answer = call.data.split("split")
            current_col = int(answer[2])
            registred_row = int(answer[1])
            user_id = call.message.chat.id
            user_message = call.message
            coodinates = "split" + str(registred_row) + "split" + str(current_col)
            # Функция для ввода секций
            if answer[0] in ["Хочу в IT", "Уже в IT", "Биохим"]:
                section = answer[0]
                worksheet.update_cell(registred_row, current_col, section)

                if answer[0] == "Хочу в IT":
                    current_col += 1
                    question = worksheet.cell(1, current_col).value
                    menu = telebot.types.InlineKeyboardMarkup()
                    menu.add(telebot.types.InlineKeyboardButton(text = 'Аналитика', callback_data ='Аналитика' + coodinates + "split" + section))
                    menu.add(telebot.types.InlineKeyboardButton(text = 'Разработка', callback_data ='Разработка' + coodinates + "split" + section))
                    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text="🟡 " + "Выберете пре-секцию:", reply_markup=menu)


                elif answer[0] == "Уже в IT":
                    current_col += 1
                    bot.send_message(user_id, "Твой ответ: "+ str(answer[0]))
                    get_question(call.message, current_col + 1, registred_row)
                    bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup = '')

                else:
                    current_col += 1
                    question = worksheet.cell(1, current_col).value
                    menu = telebot.types.InlineKeyboardMarkup()
                    menu.add(telebot.types.InlineKeyboardButton(text = 'Фармацевтика', callback_data ='Фармацевтика' + coodinates + "split" + section))
                    menu.add(telebot.types.InlineKeyboardButton(text = 'Биотехнологии', callback_data ='Биотехнологии' + coodinates + "split" + section))
                    menu.add(telebot.types.InlineKeyboardButton(text = 'Энергетика и Нефтегаз', callback_data ='Нефтегаз' + coodinates + "split" + section))
                    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text="🟡 " + question, reply_markup=menu)
            
            elif answer[0] in ["Аналитика","Разработка"]:
                section = answer[0]
                question = worksheet.cell(1, current_col).value
                menu = telebot.types.InlineKeyboardMarkup()
                if answer[0] == "Аналитика":
                    menu.add(telebot.types.InlineKeyboardButton(text = 'System&Business аналитика', callback_data ='System&Business' + coodinates + "split" + section))
                    menu.add(telebot.types.InlineKeyboardButton(text = 'Product&Data аналитика', callback_data ='Product&Data' + coodinates + "split" + section))
                    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text="🟡 " + question, reply_markup=menu)
                if answer[0] == "Разработка":
                    menu.add(telebot.types.InlineKeyboardButton(text = 'Frontend разработка', callback_data ='Frontend' + coodinates + "split" + section))
                    menu.add(telebot.types.InlineKeyboardButton(text = 'Backend разработка', callback_data ='Backend' + coodinates + "split" + section))
                    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text="🟡 " + question, reply_markup=menu)
                

            elif answer[0] in ["123"]:
                if answer[0] in ["System&Business","Product&Data", "Frontend", "Backend"]:
                    current_col += 1
                    worksheet.update_cell(registred_row, current_col, str(answer[0]))  # Update the answer in the worksheet

                else:
                    current_col += 1
                    worksheet.update_cell(registred_row, current_col, str(answer[0]))  # Update the answer in the worksheet
                    current_col += 2
                section = answer[3]
                # Send the user to the next question after the answer is received
                bot.send_message(user_id, "Твой ответ: "+ str(answer[0]) +" в секции " + str(section))
                bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup = '')
                get_question(call.message, current_col + 1, registred_row)

            # Функция для ввода другого
            elif answer[0] == "Другой":
                bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup = '')
                bot.send_message(user_id, "Пожалуйста, введите свой ответ")
                bot.register_next_step_handler(call.message, save_other, registred_row, current_col)
            
            # Функция для ввода амбассадоров
            elif answer[0] == "Амбассадор":
                bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup = '')
                bot.send_message(user_id, "Введи @ в телеграмме амбассадора, от которого ты прошёл. Если же не знаешь, то ставь прочерк")
                worksheet.update_cell(registred_row, current_col, answer[0])  # Update the answer in the worksheet
                bot.register_next_step_handler(call.message, save_ambassador, registred_row, current_col)
            
            # Функция для ввода амбассадоров
            elif answer[0] == "Друзья":
                bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup = '')
                bot.send_message(user_id, "Введи id друга, от которого ты прошёл. Если же не знаешь, то ставь прочерк")
                worksheet.update_cell(registred_row, current_col, answer[0])  # Update the answer in the worksheet
                bot.register_next_step_handler(call.message, save_friends, registred_row, current_col)

            else:
                # Карьерная гостнка
                if answer[0] in ["Хочу", "Не хочу", "Потом"]:
                    current_col = 18
                # Амбассадорство
                if answer[0] in ["Амбассадорство", "Отказ"]:
                    current_col = 21
                # Бал амбассадором?
                if answer[0] in ["Был","Впервые"]:
                    current_col = 23
                # Про персональные данные
                if answer[0] in ["Согласен"]:
                    current_col = 27

                worksheet.update_cell(registred_row, current_col, answer[0])  # Update the answer in the worksheet

                if answer[0] in ["Потом", "Не хочу"]:
                    current_col = 20
                if answer[0] == "Амбассадорство":
                        current_col = 22
                elif answer[0] == "Отказ":
                        current_col = 26
                if answer[0] in ["Москва","Московская область"]:
                    current_col += 1
                if answer[0] == "Да, хочу":
                    current_col += 2
                # Send the user to the next question after the answer is received
                bot.send_message(user_id, "Твой ответ: " + str(answer[0]))
                bot.edit_message_reply_markup(user_id, call.message.message_id, reply_markup = '')
                get_question(user_message, current_col + 1, registred_row)
    except Exception as e:
        bot.send_message(call.message.chat.id, 'Произошла ошибка. Пожалуйста, попробуйте еще раз.')
        print(f"Error while getting callback: {e}")
        start_button(call.message.chat.id)



# Функция для начала регистрации
@bot.message_handler(func=lambda message: message.text == "Регистрация")
def start_registration(message):
    user_id = message.chat.id
    if check_spam(user_id):
        if is_registered(message.chat.id):

            bot.send_message(message.chat.id, 'Вы уже зарегистрированы!')
        else:
            # remove = telebot.types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, 'Регистрация закончена')
            # current_col = 3  # Сбрасываем номер текущей строки
            # registred_row = int(worksheet.col_values(75)[len(worksheet.col_values(75))-1])
            # worksheet.update_cell(registred_row + 1, 75, registred_row + 1)
            # get_question(message, current_col+1, registred_row)
            # worksheet.update_cell(registred_row, 3, message.chat.username)
            # worksheet.update_cell(registred_row, 2, message.chat.id)
            # worksheet.update_cell(registred_row, 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, дождитесь ответа на предыдущий вопрос')


# Функция для проверки статуса регистрации
@bot.message_handler(func=lambda message: message.text == "Статус регистрации")
def status(message):
    try:
        id = worksheet_registration.col_values(2).index(str(message.chat.id))
        bot.send_message(message.chat.id, worksheet_registration.acell("D" + str(id+1)).value)
        if worksheet_registration.acell("D" + str(id+1)).value == "Поздравляем, ты прошёл отбор!🥳" or worksheet_registration.acell("D" + str(id+1)).value == "Поздравляем, ты прошла отбор!🥳":
            bot.send_message(message.chat.id, "Ссылка на вступление в чат: https://t.me/+0o0QVL0Cx1hjMTVi")

    except Exception as e:
            bot.send_message(message.chat.id, 'Произошла ошибка. Пожалуйста, попробуйте еще раз или напишите в поддержку для проверка статуса регистрации.')
            print(f"Error while getting question: {e}")
            start_button(message.chat.id)



# Функция для вывода социальных сетей
@bot.message_handler(func=lambda message: message.text == "Наши социальные сети!")
def Social_media(message):
    bot.send_message(message.chat.id,"Группа в ВК - https://vk.com/breakpoint\nТГ канал - https://t.me/forumbreakpoint\nInstagram* - forumbreakpoint : https://instagram.com/forumbreakpoint?igshid=NTc4MTIwNjQ2YQ==\nЮтуб канал - https://youtube.com/@BreakPointForum\n\nОбязательно подпишись на все соц.сети, ведь в каждой публикуется уникальный контент🔥\n\n*Meta и Instagram - запрещённые в Российской федереции организации")

# Функция для вывода контактов менеджеров (идея: можно предлагать писать в бота и сохранять в google sheets)
@bot.message_handler(func=lambda message: message.text == "Поддержка")
def problems(message):
    bot.send_message(message.chat.id, 'Наша команда менеджеров готова выслушать твои предложения или помочь решить проблемы, которые у тебя могли возникнуть:\nАнастасия - @leananastya\nАнгелина - @dreamange\nДиана - @dirmnk\nИрина - @irakharitonovaa')
    bot.send_message(message.chat.id, 'Спасибо, что помогаешь нам улучшать наш сервис!❤️')

def send(users):
    number = 0
    text = '''
Объявляем бинго на развитие вашей карьеры🔥🤌

Именно то зачем мы здесь собрались! Кто первый выполнит все задания из бинго получит призы на закрытие 2 дня😎

Как выполните все задания, присылайте в лс @lizturova подтверждения.

Ссылки на стажировки от компаний:
- https://edu.rosatom.ru/ - гринатом
– https://sbergraduate.ru/sberseasons-moscow/ - sber
– https://docs.google.com/forms/d/e/1FAIpQLSe_etLfepeyMzb9ztY9-Yx_finJnNMFfcG3Rmt0eqRez-DBVA/viewform?usp=send_form - Bearningpoint
'''
    # users = [ADMIN_ID]
    bot.send_message(ADMIN_ID,"Началась рассылка")
    for i in set(users):
        try:
            if number == 15:
                time.sleep(10)
                number = 0
            #menu = telebot.types.InlineKeyboardMarkup()
            #menu.add(telebot.types.InlineKeyboardButton(text = 'Буду', callback_data ='Буду'))
            #menu.add(telebot.types.InlineKeyboardButton(text = 'К сожалению, не смогу;(', callback_data ='К сожалению, не смогу;('))
            bot.send_message(i, text=text)
            programm_send_1("Бинго",i=i)
            number += 1
            bot.send_message(ADMIN_ID,i)
        except:
            bot.send_message(ADMIN_ID,f'{i} ливнул')
    bot.send_message(ADMIN_ID,"Закончилась рассылка")

@dp.message_handler(func=lambda message: message.text == "Триггер")
def send_message_to_users(message):
    if str(message.chat.id) == ADMIN_ID:
        users = worksheet_send.col_values(3)
        send(users)

@dp.message_handler(func=lambda message: message.text == "Назад")
def return_back(message):
    start_button(message.chat.id)

@bot.message_handler(func=lambda message: message.text in ["IT (Общая)","BioChem (Общая)","System&Business аналитика","Product&Data аналитика","Frontend разработка","Backend разработка"])
def programm_send(message):
    if message.text == "IT (Общая)":
            bot.send_media_group(message.chat.id, [telebot.types.InputMediaPhoto(open(photo, 'rb')) for photo in ['ИТ.jpg']])
    if message.text == "BioChem (Общая)":
            bot.send_media_group(message.chat.id, [telebot.types.InputMediaPhoto(open(photo, 'rb')) for photo in ['Биохим.jpg']])
    if message.text == "System&Business аналитика":
            bot.send_media_group(message.chat.id, [telebot.types.InputMediaPhoto(open(photo, 'rb')) for photo in ['Бизнес-1день.jpg','Бизнес-2день.jpg']])
    if message.text == "Product&Data аналитика":
            bot.send_media_group(message.chat.id, [telebot.types.InputMediaPhoto(open(photo, 'rb')) for photo in ['Продакт-1день.jpg','Продакт-2день.jpg']])
    if message.text == "Frontend разработка":
            bot.send_media_group(message.chat.id, [telebot.types.InputMediaPhoto(open(photo, 'rb')) for photo in ['Фронт-1день.jpg','Фронт-1день.jpg']])
    if message.text == "Backend разработка":
            bot.send_media_group(message.chat.id, [telebot.types.InputMediaPhoto(open(photo, 'rb')) for photo in ['Бэк-1день.jpg','Бэк-1день.jpg']])

@bot.message_handler(func=lambda message: message.text in ["Бинго"])
def programm_send_1(message,i):
    if message == "Бинго":
        bot.send_media_group(i, [telebot.types.InputMediaPhoto(open(photo, 'rb')) for photo in ['бинго.jpeg']])
    

@bot.message_handler(func=lambda message: message.text == "Программа")
def programm(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    btn1 = telebot.types.KeyboardButton("IT (Общая)")
    btn2 = telebot.types.KeyboardButton("BioChem (Общая)")
    btn3 = telebot.types.KeyboardButton("System&Business аналитика")
    btn4 = telebot.types.KeyboardButton("Product&Data аналитика")
    btn5 = telebot.types.KeyboardButton("Frontend разработка")
    btn6 = telebot.types.KeyboardButton("Backend разработка")
    btn7 = telebot.types.KeyboardButton("Назад")
    markup.row(btn1,btn2)
    markup.row(btn3,btn4)
    markup.row(btn5,btn6)
    markup.row(btn7)
    bot.send_message(message.chat.id, "Меню:",reply_markup=markup)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    text1 = '''
        Привет! На связи команда организаторов форума BreakPoint 👋
        
        BreakPoint — всероссийский форум для студентов и выпускников технических и IT направлений. Форум для людей, влияющих на технологии и процессы, которые происходят в России и в мире.
        
Форум включает в себя:
        - Сессии (выступления топовых спикеров в сфере IT, Биохима и технологий)
        - Воркшопы и бизнес-кейсы (интерактивные сессии и бизнес-игры от компаний-партнёров)
        - Digital карьерную гостиную (короткие онлайн-собеседования с HR-специалистами компаний-партнёров с возможностью дальнейшего трудоустройства)
        
        Участие в форуме бесплатное! Все, что нужно - это заполнить данную заявку и пройти отбор.
        Просим тебя отвечать на вопросы внимательно, развёрнуто и искренне 😌
        
        Подробнее о событии ты можешь узнать в группе  (https://vk.com/breakpoint).
Если у тебя возникли вопросы, пиши руководителю департамента по работе с участниками Валько Никите: @Maine767)
        '''
    text2 = '''
        Всего несколько блоков вопросов:
    1. Для всех - 12 вопросов
    2. Вопросы:
      a)Для 'Хочу в IT' - +1 вопрос
      б)Для 'Уже в IT' - +2 вопроса
      в)Для ребят не из МСК - +1 вопрос
          
Среднее время заполнения формы: 5 минут
'''
    bot.send_message(message.chat.id, text1)
    bot.send_message(message.chat.id, text2)

    start_button(message.chat.id)



def start_button(user_id):
    markup = telebot.types.ReplyKeyboardMarkup()

    if not is_registered(user_id):
        btn1 = telebot.types.KeyboardButton("Регистрация")
        markup.row(btn1)
    btn2 = telebot.types.KeyboardButton("Статус регистрации")
    btn3 = telebot.types.KeyboardButton("Поддержка")
    btn4 = telebot.types.KeyboardButton("Наши социальные сети!")
    btn6 = telebot.types.KeyboardButton("Программа")
    if str(user_id) == ADMIN_ID:  
        btn5 = telebot.types.KeyboardButton("Триггер")
        markup.row(btn2, btn3, btn4)
        markup.row(btn5)
        markup.row(btn6)
    else:
        markup.row(btn2, btn3, btn4)
        markup.row(btn6)
    bot.send_message(user_id, "Меню:",reply_markup=markup)


# Обработка текста на спам
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_message(message):
    user_id = str(message.from_user.id)

    if check_spam(user_id):
        # Ваша обработка текстовых сообщений здесь
        pass
    else:
        print(user_id)
        block_user(user_id, 12)
        bot.send_message(message.chat.id, 'Пожалуйста, дождитесь ответа на предыдущий вопрос')


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
