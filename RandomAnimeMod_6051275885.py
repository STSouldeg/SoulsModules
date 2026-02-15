# meta developer: @aethergeminibot
from .. import loader, utils
import aiohttp
import logging

logger = logging.getLogger(__name__)

@loader.tds
class RandomAnimeMod(loader.Module):
    """Модуль для генерации случайных аниме-персонажей"""
    strings = {"name": "RandomAnime"}

    @loader.command()
    async def ranime(self, message):
        """Прислать фото случайного аниме-персонажа"""
        await utils.answer(message, "🌸 **Ищу вайфу...**")
        
        try:
            async with aiohttp.ClientSession() as session:
                # Используем надежное API для аниме-артов
                async with session.get("https://nekos.best/api/v2/neko") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        result = data.get('results', [{}])[0]
                        image_url = result.get('url')
                        artist = result.get('artist_name', 'Unknown')
                        
                        await self._client.send_file(
                            message.peer_id, 
                            image_url, 
                            caption=f"🏮 **Твой аниме-персонаж готов!**\n🎨 *Художник:* {artist}"
                        )
                        await message.delete()
                    else:
                        await utils.answer(message, "❌ API временно недоступно, попробуй позже.")
        except Exception as e:
            logger.error(f"Anime error: {e}")
            await utils.answer(message, f"❌ Ошибка при загрузке: {str(e)}")