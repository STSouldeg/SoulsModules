# meta developer: @aethergeminibot
from .. import loader, utils
import random
import logging

logger = logging.getLogger(__name__)

@loader.tds
class RussianMemeMod(loader.Module):
    """Модуль для получения русских мемов напрямую из TG"""
    strings = {"name": "RandomMeme"}

    @loader.command()
    async def meme(self, message):
        """Прислать случайный мем из топовых каналов"""
        await utils.answer(message, "🇷🇺 **Листаю ленту мемов...**")
        
        try:
            # Список проверенных каналов с мемами
            channels = ['memes_rus', 'prikol', 'leprum', 'mudak', 'vine_rus', 'i_m_h_o']
            target_channel = random.choice(channels)
            
            # Получаем последние 100 сообщений из выбранного канала
            messages = await self._client.get_messages(target_channel, limit=100)
            
            # Фильтруем сообщения, в которых есть фото
            photo_messages = [m for m in messages if m.photo]
            
            if not photo_messages:
                await utils.answer(message, "❌ Не удалось найти картинки в этом канале. Попробуй еще раз.")
                return

            # Выбираем случайный пост с фото
            target = random.choice(photo_messages)
            
            # Отправляем фото пользователю
            await self._client.send_file(
                message.peer_id, 
                target.photo, 
                caption=f"🤣 **Свежий мем из сети**\n\n📌 *Источник: @{target_channel}*"
            )
            await message.delete()
            
        except Exception as e:
            logger.error(f"Meme error: {e}")
            await utils.answer(message, "❌ Ошибка доступа к каналам. Попробуй позже.")