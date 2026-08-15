import telebot
from random import randint
from config import token
from logic import Pokemon, Wizard, Fighter

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['go'])
def go(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        # Уменьшенный шанс супер-покемонов (примерно 20 %)
        chance = randint(1, 10)
        if chance <= 8:          # 80 % — обычный
            pokemon = Pokemon(message.from_user.username)
        elif chance == 9:        # 10 % — Wizard
            pokemon = Wizard(message.from_user.username)
        else:                    # 10 % — Fighter
            pokemon = Fighter(message.from_user.username)

        bot.send_message(message.chat.id, pokemon.info())
        if pokemon.show_img():
            bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "Ты уже создал себе покемона!")


@bot.message_handler(commands=['info'])
def info(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[message.from_user.username]
        bot.send_message(message.chat.id, pokemon.info())
        if pokemon.show_img():
            bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "Сначала создай покемона командой /go")



@bot.message_handler(commands=['train'])
def train(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[message.from_user.username]
        pokemon.train()
        bot.send_message(message.chat.id, "Покемон потренировался и стал сильнее!")
        bot.send_message(message.chat.id, pokemon.info())
    else:
        bot.reply_to(message, "Сначала создай покемона командой /go")


@bot.message_handler(commands=['restore'])
def restore(message):
    """Восстановление силы покемона"""
    if message.from_user.username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[message.from_user.username]
        pokemon.power = randint(20, 40)          # восстанавливаем силу
        bot.send_message(message.chat.id, "Сила покемона восстановлена!")
        bot.send_message(message.chat.id, pokemon.info())
    else:
        bot.reply_to(message, "Сначала создай покемона командой /go")


@bot.message_handler(commands=['attack'])
def attack_pok(message):
    if message.reply_to_message:  # команда должна быть ответом на сообщение
        attacker_name = message.from_user.username
        enemy_name = message.reply_to_message.from_user.username

        if (attacker_name in Pokemon.pokemons.keys() and
            enemy_name in Pokemon.pokemons.keys()):

            if attacker_name == enemy_name:
                bot.send_message(message.chat.id, "Нельзя атаковать самого себя!")
                return

            pok = Pokemon.pokemons[attacker_name]
            enemy = Pokemon.pokemons[enemy_name]

            result = pok.attack(enemy)
            bot.send_message(message.chat.id, result)
            bot.send_message(message.chat.id, f"Твой покемон:\n{pok.info()}")
            bot.send_message(message.chat.id, f"Покемон противника:\n{enemy.info()}")
        else:
            bot.send_message(message.chat.id, "Сражаться можно только с теми, у кого есть покемон")
    else:
        bot.send_message(message.chat.id, "Чтобы атаковать, нужно ответить на сообщение соперника командой /attack")

@bot.message_handler(commands=['feed'])
def feed_pok(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pokemon = Pokemon.pokemons[message.from_user.username]
        result = pokemon.feed()
        bot.send_message(message.chat.id, result)
        bot.send_message(message.chat.id, pokemon.info())
    else:
        bot.reply_to(message, "Сначала создай покемона командой /go")
@bot.message_handler(commands=['fightnpc'])
def fight_npc(message):
    username = message.from_user.username

    if username not in Pokemon.pokemons.keys():
        bot.reply_to(message, "Сначала создай покемона командой /go")
        return

    pok = Pokemon.pokemons[username]

    # Создаём случайного NPC
    chance = randint(1, 3)
    if chance == 1:
        npc = Pokemon("NPC")
    elif chance == 2:
        npc = Wizard("NPC")
    else:
        npc = Fighter("NPC")

    # Проводим бой
    result = pok.attack(npc)

    # Удаляем NPC из словаря, чтобы не засорять
    if "NPC" in Pokemon.pokemons:
        del Pokemon.pokemons["NPC"]

    # Отправляем результат
    bot.send_message(message.chat.id, f"⚔️ Бой с NPC!\n\n{result}")
    bot.send_message(message.chat.id, f"Твой покемон:\n{pok.info()}")
    bot.send_message(message.chat.id, f"Покемон NPC:\n{npc.info()}")
    
bot.infinity_polling(none_stop=True)