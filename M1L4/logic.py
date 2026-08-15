from random import randint, choice
from datetime import datetime, timedelta
import requests


class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = randint(1, 1000)

        self.img = self.get_img()
        self.name = self.get_name()
        self.height = self.get_height()
        self.weight = self.get_weight()
        self.types = self.get_types()

        # Система уровней
        self.level = 1
        self.battles = 0
        self.max_hp = 100
        self.hp = choice([55, 65, 80, 90, 95, 100])
        self.power = randint(10, 30)

        # Кормление
        self.last_feed_time = datetime.now() - timedelta(seconds=100)
        self.feed_interval = 20          # секунд
        self.feed_amount = 10

        Pokemon.pokemons[pokemon_trainer] = self

    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['sprites']["other"]["home"]['front_default']
        return None

    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['forms'][0]['name']
        return "Pikachu"

    def get_height(self):
        url = f"https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data["height"]
        return 0

    def get_weight(self):
        url = f"https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data["weight"]
        return 0

    def get_types(self):
        url = f"https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return [t["type"]["name"] for t in data["types"]]
        return []

    def info(self):
        return (
            f"Имя: {self.name}\n"
            f"Уровень: {self.level}\n"
            f"Тип: {', '.join(self.types)}\n"
            f"Рост: {self.height}\n"
            f"Вес: {self.weight}\n"
            f"HP: {self.hp}/{self.max_hp}\n"
            f"Сила: {self.power}\n"
            f"Боёв: {self.battles}"
        )

    def show_img(self):
        return self.img

    def heal(self):
        self.hp = self.max_hp

    def damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def change_trainer(self, trainer):
        del Pokemon.pokemons[self.pokemon_trainer]
        self.pokemon_trainer = trainer
        Pokemon.pokemons[trainer] = self

    def train(self):
        boost = randint(1, 10)
        self.power += boost

    def attack(self, enemy):
        # Щит волшебника
        if isinstance(enemy, Wizard):
            chance = randint(1, 5)
            if chance == 1:
                return "Покемон-волшебник применил щит в сражении"

        if enemy.hp > self.power:
            enemy.hp -= self.power
            result = f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}"
        else:
            enemy.hp = 0
            result = f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}! "

        # Система уровней
        self.battles += 1
        level_up_msg = ""

        if self.battles % 5 == 0:
            self.level += 1
            self.max_hp += 10
            power_boost = randint(3, 7)
            self.power += power_boost
            self.hp = self.max_hp

            level_up_msg = (
                f"\n\n🎉 LEVEL UP! 🎉\n"
                f"Новый уровень: {self.level}\n"
                f"+10 к максимальному HP (теперь {self.max_hp})\n"
                f"+{power_boost} к силе (теперь {self.power})"
            )

        return result + level_up_msg

    def feed(self):
        now = datetime.now()
        time_passed = now - self.last_feed_time

        if time_passed >= timedelta(seconds=self.feed_interval):
            self.hp += self.feed_amount
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            self.last_feed_time = now
            return f"Покемон покормлен! +{self.feed_amount} HP\nСейчас HP: {self.hp}/{self.max_hp}"
        else:
            next_time = self.last_feed_time + timedelta(seconds=self.feed_interval)
            remaining = next_time - now
            seconds_left = int(remaining.total_seconds())
            return (f"Кормить пока рано!\n"
                    f"Следующее кормление через {seconds_left} сек.\n"
                    f"({next_time.strftime('%H:%M:%S')})")


class Wizard(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.feed_amount = 20          # Волшебник восстанавливает больше HP

    def feed(self):
        return super().feed()


class Fighter(Pokemon):
    def __init__(self, pokemon_trainer):
        super().__init__(pokemon_trainer)
        self.feed_interval = 10        # Боец имеет меньший интервал кормления

    def attack(self, enemy):
        super_power = randint(5, 15)
        self.power += super_power
        result = super().attack(enemy)
        self.power -= super_power
        return result + f"\nБоец применил супер-атаку силой: {super_power}"

    def feed(self):
        return super().feed()