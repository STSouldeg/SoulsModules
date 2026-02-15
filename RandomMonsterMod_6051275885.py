
# meta developer: @aethergeminibot
from .. import loader, utils
import random

class RandomMonsterMod(loader.Module):
    """Модуль для генерации случайных монстров"""
    strings = {"name": "RandomMonster"}

    @loader.command()
    async def scarycmd(self, message):
        """Прислать фото случайного монстра"""
        await message.edit("👹 <i>Призываю монстра...</i>")
        seed = random.randint(1, 100000)
        # Используем проверенный RoboHash (set2 - это монстры)
        url = f"https://robohash.org/{seed}.png?set=set2"
        await message.client.send_file(message.chat_id, url, caption="👹 Бу!")
        await message.delete()