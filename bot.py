import telebot
import random
from time import time
from datetime import datetime, timedelta
from questions import questions

bot = telebot.TeleBot('5533989507:AAEGWwkzawMMy9yCXAGvPhMtFi9GrsK6-hM')

    #кількість правильних відповідей
score = 0

    #глобальна змінна для відслідковування на якому запитанні ми зараз знаходимося
curentQuestion = questions[0]

    #використовується для того щоб бот очікував на повідомлення від користувача
flag = 1

    #після того, як завершився тест, бот буде реагувати лише на команду /start а потім на всі повідомлення і так по кругу
compete = 0

    #перевірка на правильну відповідь
def check_choise(id, choise_id):
    global score, curentQuestion, flag, compete

    #перевірка на те чи завершили ми вже тест
    if not compete:
        if curentQuestion.checkAnsw(curentQuestion.choises[int(choise_id)]):
            bot.send_message(
                id,
                'правильно \u2714'
            )

            score += 1
        else:
            bot.send_message(
                id,
                'неравильно \u274C\n' +
                f'правильна відповідь: {curentQuestion.answer}'
            )

        flag = 0


    #ініціалізація reply клавіатури
def set_markup():
    global curentQuestion

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    itembtn1 = telebot.types.KeyboardButton(f'1. {curentQuestion.choises[0]}')
    itembtn2 = telebot.types.KeyboardButton(f'2. {curentQuestion.choises[1]}')
    itembtn3 = telebot.types.KeyboardButton(f'3. {curentQuestion.choises[2]}')
    itembtn4 = telebot.types.KeyboardButton(f'4. {curentQuestion.choises[3]}')

    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

    return markup


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "привіт! бажаєш перевірити свої знання по python? розпочнемо!")
    global score, curentQuestion, flag, compete
    compete = 0

    random.shuffle(questions)

    score = 0
    start = round(time())

    for question in questions:
        random.shuffle(question.choises)
        curentQuestion = question

        bot.send_message(
            message.chat.id,
            question.question,
            reply_markup=set_markup()
        )

        #використовується для того, щоб бот очікував на повідомлення від користувача
        while flag == 1:
            pass

        flag = 1

    end = round(time()) - start
    end = timedelta(seconds = end)

    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    bot.send_message(
        message.chat.id,
        'вітаю - тест пройдено!\n' +
        f'дата та час виконання: {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}.\n' +
        f'час виконання: {str(end)}. результат: {score} із 10\n',
        reply_markup=markup
    )

    compete = 1


@bot.message_handler()
def check_ans(message):
    if message.text.startswith('1'):
        id = 0
    elif message.text.startswith('2'):
        id = 1
    elif message.text.startswith('3'):
        id = 2
    elif message.text.startswith('4'):
        id = 3
    else:
        return

    check_choise(message.chat.id, id)


bot.polling(none_stop=True)
