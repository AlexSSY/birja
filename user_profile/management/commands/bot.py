from django.core.management.base import BaseCommand
import telebot

from ...models import BotaModel

class Command(BaseCommand):
    help = 'Telegram BOT'

    def handle(self, *args, **options):
        token = "6131628795:AAF_HM9FhpsbsvY89WWRLO-WQGjmZuqJafk"
        bot = telebot.TeleBot(token)

        msg1 = ""
        msg2 = ""
        msg3 = ""
        id = 0

        ADMINS = [
            5235364536,
        ]
    
        @bot.message_handler(commands=["start"])
        def start_message(message):
            id = message.from_user.id
            bot.send_message(message.chat.id, "Привет вас приветствует Tera Trade.")
            bot.send_message(message.chat.id, "❗️ Имеете ли вы опыт в скаме или трафе, ответьте подробно:", parse_mode="html")
            bot.register_next_step_handler(message, get_message_1)
            

        def get_message_1(message):
            msg1 = message.text
            bot.send_message(message.chat.id, "❗️ Ссылка на ваш профиль с форума где вы нашли нашу тему. (DARK2WEB, CENTER, YOUHACK и подобные):")
            bot.register_next_step_handler(message, get_message_2)


        def get_message_2(message):
            msg2 = message.text
            bot.send_message(message.chat.id, "❗️ Знание языков и уровень владения:")
            bot.register_next_step_handler(message, get_message_3)


        def get_message_3(message):
            msg3 = message.text
            try:
                BotaModel(
                    message1=msg1,
                    message2=msg2,
                    message3=msg3,
                    user_id = id
                ).save()
                bot.send_message(message.chat.id, "❗️ Ваша заявка отправленна на рассмотрение.")
            except Exception as e:
                bot.send_message(message.chat.id, "❗️ Ошибка: Вы уже отправляли заявку (<i>отправить заявку повторно вы сможете лишь на следующий день после отказа</i>)"
                    , parse_mode="html")


        bot.set_my_commands(commands=[
            telebot.types.BotCommand("start", "Начать работу"),
        ])

        bot.infinity_polling()
