import token
import aiohttp
import random
from datetime import datetime, timedelta

class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.name = None
        self.hp = random.randint(200, 400)
        self.power = random.randint(30, 60)
        self.last_feed_time = datetime.now()
        self.img = None

        if pokemon_trainer not in Pokemon.pokemons:
            Pokemon.pokemons[pokemon_trainer] = self
        else:
            self = Pokemon.pokemons[pokemon_trainer] 

    async def feed(self, feed_interval= 20, hp_increase=10):
        current_time = datetime.now() 
        delta_time = timedelta(hours=feed_interval) 
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time 
            return (f"Pokémon sağlığı geri yüklenir. Mevcut HP: {self.hp}")
        else:
            return (f"Pokémonunuzu şu zaman besleyebilirsiniz:{self.last_feed_time + delta_time }")

    # API'den tüm verileri tek seferde çeken yardımcı metot
    async def get_data(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    self.name = data['forms'][0]['name'].capitalize()
                    self.img = data['sprites']['front_default']
                    # API'den ekstra nitelikler (Örn: Can ve Saldırı)
                else:
                    self.name = "Pikachu"

    # Bilgi döndüren metot
    async def info(self):
        if not self.name:
            await self.get_data()
        return f"Pokémonunuzun ismi: {self.name}\nCan (HP): {self.hp}\nGüç: {self.power}"

    # Görsel URL'sini döndüren metot
    async def show_img(self):
        if not self.img:
            await self.get_data()
        return self.img

    async def attack(self, enemy):
        if isinstance(enemy, Wizard):  # Düşmanın Wizard veri tipi olup olmadığının kontrol edilmesi (Sihirbaz sınıfının bir örneği midir?) 
            sans = random.randint(1, 5) 
            if sans == 1:
                return "Sihirbaz Pokémon, savaşta bir kalkan kullanıldı!"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ne saldırdı\n@{enemy.pokemon_trainer}'nin sağlık durumu {enemy.hp}"
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ni yendi!"


class Wizard (Pokemon):
    async def feed(self):
        return await super().feed(hp_increase=20)

class Fighter (Pokemon):
    async def attack(self, enemy):
        super_guc = random.randint(5, 15)  
        self.guc += super_guc
        sonuc = await super().attack(enemy)  
        self.guc -= super_guc
        return sonuc + f"\nDövüşçü Pokémon süper saldırı kullandı. Eklenen güç: {super_guc}"

    async def feed(self):
        return await super().feed(feed_interval=10)

