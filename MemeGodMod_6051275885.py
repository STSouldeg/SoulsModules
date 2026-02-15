# meta developer: @aethergeminibot
from .. import loader, utils
import random
import logging

logger = logging.getLogger(__name__)

@loader.tds
class MemeGodMod(loader.Module):
    """Ультимативный модуль для русских мемов с защитой от ошибок"""
    strings = {"name": "RandomMeme"}

    @loader.command()
    async def meme(self, message):
        """Прислать случайный мем (с автоподбором рабочего канала)"""
        await utils.answer(message, "🇷🇺 **Ищу живой канал с мемами...**")
        
        # Список проверенных каналов
        channels = ['memes_rus', 'prikol', 'leprum', 'mudak', 'vine_rus', 'i_m_h_o', 'ru_python_memes', 'pozorniy_prizrak']
        random.shuffle(channels) # Перемешиваем, чтобы не долбиться в один и тот же
        
        success = False
        for channel in channels:
            try:
                # Пытаемся получить последние сообщения
                msgs = await self._client.get_messages(channel, limit=50)
                # Фильтруем только фото
                photos = [m for m in msgs if m.photo]
                
                if photos:
                    target = random.choice(photos)
                    await self._client.send_file(
                        message.peer_id, 
                        target.photo, 
                        caption=f"🤣 **Твой мем готов!**\n\n📌 *Источник: @{channel}*"
                    )
                    await message.delete()
                    success = True
                    break # Выходим из цикла, если все ок
            except Exception as e:
                logger.warning(f"Channel @{channel} failed: {e}")
                continue # Пробуем следующий канал
        
        if not success:
            await utils.answer(message, "❌ Все источники временно недоступны. Попробуй через 5 минут.")