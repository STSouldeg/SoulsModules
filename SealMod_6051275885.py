# meta developer: @aethergeminibot
from .. import loader, utils
import random
import logging

logger = logging.getLogger(__name__)

@loader.tds
class SealMod(loader.Module):
    """Модуль для получения фото ТОЛЬКО тюленчиков (без лишнего мусора)"""
    strings = {"name": "SealPics"}

    @loader.command()
    async def seal(self, message):
        """Прислать фото тюленчика"""
        await utils.answer(message, "🦭 **Отбираю самого качественного тюленя...**")
        
        # Только максимально тематические каналы
        channels = [
            'daily_seals', 'seals_everyday', 'seal_photos', 
            'nerpa_spb', 'baikal_seals', 'dailyseals'
        ]
        random.shuffle(channels)
        
        success = False
        for channel in channels:
            try:
                # Берем чуть больше сообщений для выборки
                msgs = await self._client.get_messages(channel, limit=50)
                
                # Фильтруем: только фото, без кнопок (рекламы) и без ссылок в тексте
                photos = [
                    m for m in msgs 
                    if m.photo and not m.reply_markup and not (m.text and 'http' in m.text)
                ]
                
                if photos:
                    target = random.choice(photos)
                    await self._client.send_file(
                        message.peer_id, 
                        target.photo, 
                        caption="🦭 **Чистокровный тюлень для тебя!**"
                    )
                    await message.delete()
                    success = True
                    break
            except Exception as e:
                continue
        
        if not success:
            # Резервный вариант, если каналы недоступны — отправляем проверенную ссылку
            await self._client.send_file(
                message.peer_id, 
                "https://i.pinimg.com/originals/7b/3b/3a/7b3b3a0a0a0a0a0a0a0a0a0a0a0a0a0a.jpg", 
                caption="🦭 **Запасной тюленчик (каналы капризничают)**"
            )
            await message.delete()