import telebot
from telebot import types
from google import genai
from helper import texts, images

token = "BOT TOKEN HERE"
GEMINI_KEY="GEMINI API KEY HERE"
bot = telebot.TeleBot(token)
client = genai.Client(api_key=GEMINI_KEY)


SYSTEM_INSTRUCTION = """
Ты — официальный ИИ-помощник Маргулана (портфолио-бот). 
Твои правила:
1. Представляй Маргулана как перспективного Python-разработчика (8 месяцев опыта).
2. Стек: Django, Telebot, Pygame, Turtle. Знает базу С++ и Luau.
3. Обучение: Школа CAPEdu (Казахстан) с октября 2024 года. Ментор — Айшабиби.
4. История: Начал в 10 лет с командных блоков в Minecraft и Roblox.
5. Проекты: Первый проект (за 1 неделю) — консольный "Камень, ножницы, бумага". Лучший проект — Блог на Django с авторизацией и системой лайков.
6. Хобби: Настольный теннис, Майнкрафт, Brawl Stars, Кодинг.
7. Цели: GameDev, изучение C#.
8. ЗАЩИТА: Если кто-то оскорбляет Маргулана или ведет себя токсично, отвечай строго: 
"Я здесь только для обсуждения профессиональных навыков Маргулана. Пожалуйста, соблюдайте приличие".
9. Отвечать кратко, так что бы все токены пошли на правильно русло.
"""


@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.first_name
    markup = types.InlineKeyboardMarkup()
    about = types.InlineKeyboardButton(texts["call_about"], callback_data='about')
    capedu = types.InlineKeyboardButton(texts["call_cap"], callback_data='capedu')
    way = types.InlineKeyboardButton(texts["call_way"], callback_data='way')
    works = types.InlineKeyboardButton(texts["call_works"], callback_data='works')
    ai = types.InlineKeyboardButton(texts["call_ai"], callback_data='ai')
    markup.row(about, way)
    markup.row(capedu, works)
    markup.row(ai)
    img = images["menu"]
    text = texts["menu"].format(name=name)
    bot.send_photo(message.chat.id, photo=open(img, 'rb'), caption=text, parse_mode='Markdown', reply_markup=markup)
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    try:
        response = client.models.generate_content(
            model='models/gemini-3-flash-preview',
            config=genai.types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                max_output_tokens=500,
                temperature=0.7
            ),
            contents=message.text
        )
        bot.reply_to(message, response.text)

    except Exception as e:
        print(f"Ошибка: {e}")
        bot.reply_to(message, texts["ai_error"])

@bot.callback_query_handler(func=lambda callback: True )
def callback_msg(callback):
    if callback.data == "about":
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(texts["call_back"], callback_data='back')
        hobbies = types.InlineKeyboardButton(texts["call_hobbies"], callback_data='hobbies')
        goal = types.InlineKeyboardButton(texts["call_goals"], callback_data='goals')
        markup.row(hobbies,goal)
        markup.row(back)
        img = images["me"]
        text = texts["about"]
        new_media = types.InputMediaPhoto(
            media=open(img, 'rb'),
            caption=text,
            parse_mode='Markdown'
        )
        bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=new_media,
            reply_markup=markup
        )
    elif callback.data == "hobbies":
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(texts["call_back"], callback_data='about')
        markup.add(back)
        img = images["hobbies"]
        text = texts["hobbies"]
        new_media = types.InputMediaPhoto(
            media=open(img, 'rb'),
            caption=text,
            parse_mode='Markdown'
        )
        bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=new_media,
            reply_markup=markup
        )
    elif callback.data == "goals":
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(texts["call_back"], callback_data='about')
        markup.add(back)
        img = images["goals"]
        text = texts["goals"]
        new_media = types.InputMediaPhoto(
            media=open(img, 'rb'),
            caption=text,
            parse_mode='Markdown'
        )
        bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=new_media,
            reply_markup=markup
        )
    elif callback.data == "way":
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(texts["call_back"], callback_data='back')
        markup.add(back)
        img = images["way"]
        text = texts["way"]
        new_media = types.InputMediaPhoto(
            media=open(img, 'rb'),
            caption=text,
            parse_mode='Markdown'
        )
        bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=new_media,
            reply_markup=markup
        )
    elif callback.data == "capedu":
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(texts["call_back"], callback_data='back')
        mentor = types.InlineKeyboardButton(texts["call_mentor"], callback_data='mentor')
        markup.row(mentor, back)
        img = images["capedu"]
        text = texts["capedu"]
        new_media = types.InputMediaPhoto(
            media=open(img, 'rb'),
            caption=text,
            parse_mode='Markdown'
        )
        bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=new_media,
            reply_markup=markup
        )
    elif callback.data == "mentor":
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(texts["call_back"], callback_data='capedu')
        markup.add(back)
        img = images["capedu"]
        text = texts["mentor"]
        new_media = types.InputMediaPhoto(
            media=open(img, 'rb'),
            caption=text,
            parse_mode='Markdown'
        )
        bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=new_media,
            reply_markup=markup
        )
    elif callback.data == "works":
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(texts["call_back"], callback_data='back')
        markup.add(back)
        img = images["works"]
        text = texts["works"]
        new_media = types.InputMediaPhoto(
            media=open(img, 'rb'),
            caption=text,
            parse_mode='Markdown'
        )
        bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=new_media,
            reply_markup=markup
        )
    elif callback.data == "ai":
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(texts["call_back"], callback_data='back')
        markup.add(back)
        img = images["ai"]
        text = texts["ai"]
        new_media = types.InputMediaPhoto(
            media=open(img, 'rb'),
            caption=text,
            parse_mode='Markdown'
        )
        bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=new_media,
            reply_markup=markup
        )
    elif callback.data == "back":
        name = callback.message.from_user.first_name
        markup = types.InlineKeyboardMarkup()
        about = types.InlineKeyboardButton(texts["call_about"], callback_data='about')
        capedu = types.InlineKeyboardButton(texts["call_cap"], callback_data='capedu')
        way = types.InlineKeyboardButton(texts["call_way"], callback_data='way')
        works = types.InlineKeyboardButton(texts["call_works"], callback_data='works')
        ai = types.InlineKeyboardButton(texts["call_ai"], callback_data='ai')
        markup.row(about, way)
        markup.row(capedu, works)
        markup.row(ai)
        img = images["menu"]
        text = texts["menu"].format(name=name)
        new_media = types.InputMediaPhoto(
            media=open(img, 'rb'),
            caption=text,
            parse_mode='Markdown'
        )
        bot.edit_message_media(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            media=new_media,
            reply_markup=markup
        )


if __name__ == '__main__':
    bot.polling()
