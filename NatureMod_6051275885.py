# meta developer: @aethergeminibot
from .. import loader, utils
import random
import logging

logger = logging.getLogger(__name__)

@loader.tds
class NatureMod(loader.Module):
    """Модуль для получения красивых фото природы и неба"""
    strings = {"name": "NaturePics"}

    @loader.command()
    async def nature(self, message):
        """Прислать красивое фото природы"""
        await utils.answer(message, "☁️ **Ищу частичку красоты для тебя...**")
        
        # Список эстетичных каналов с природой и небом
        channels = [
            'nature', 'BeautifulNaturePhotos', 'NatureGeography', 
            'earth_view', 'sky_porn', 'view_locations', 'Discovery_Geographic'
        ]
        random.shuffle(channels)
        
        success = False
        for channel in channels:
            try:
                msgs = await self._client.get_messages(channel, limit=100)
                # Ищем только качественные фото
                photos = [m for m in msgs if m.photo]
                
                if photos:
                    target = random.choice(photos)
                    await self._client.send_file(
                        message.peer_id, 
                        target.photo, 
                        caption="🌿 **Красота природы**\n\n✨ *Наслаждайся моментом*"
                    )
                    await message.delete()
                    success = True
                    break
            except Exception as e:
                logger.warning(f"Nature channel @{channel} failed: {e}")
                continue
        
        if not success:
            await utils.answer(message, "❌ Не удалось найти фото. Попробуй еще раз.")