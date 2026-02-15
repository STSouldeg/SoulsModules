# meta developer: @aethergeminibot
from .. import loader, utils
import random
import logging

logger = logging.getLogger(__name__)

@loader.tds
class RealHorrorMod(loader.Module):
    """Модуль для генерации реальных хоррор-персонажей (Джефф, Гренни и др.)"""
    strings = {"name": "RealHorror"}

    def __init__(self):
        # База прямых ссылок на классических хоррор-персонажей
        self.scary_images = [
            "https://i.imgur.com/rNfM7T4.jpg",  # Jeff the Killer
            "https://i.imgur.com/P1i1Y9W.jpg",  # Granny
            "https://i.imgur.com/vHq1FpA.jpg",  # Smile Dog
            "https://i.imgur.com/2Yy5e6F.jpg",  # Slenderman
            "https://i.imgur.com/7xXq0P9.jpg",  # Momo
            "https://i.imgur.com/E0l0v34.jpg",  # Siren Head
            "https://i.imgur.com/mOat15k.jpg",  # Pennywise
            "https://i.imgur.com/uU6mIuX.jpg"   # Nun (Valak)
        ]

    @loader.command()
    async def scary(self, message):
        """Прислать фото реального монстра/скримера"""
        await utils.answer(message, "🕯 **Призываю чистое зло...**")
        
        try:
            url = random.choice(self.scary_images)
            
            await self._client.send_file(
                message.peer_id, 
                url, 
                caption="👹 **Оно уже здесь.**"
            )
            await message.delete()
        except Exception as e:
            logger.error(f"Horror error: {e}")
            await utils.answer(message, "❌ Тьма не откликнулась...")