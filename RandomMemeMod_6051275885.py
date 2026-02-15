# meta developer: @aethergeminibot
from .. import loader, utils
import aiohttp
import logging

logger = logging.getLogger(__name__)

@loader.tds
class RandomMemeMod(loader.Module):
    """Модуль для получения русских мемов"""
    strings = {"name": "RandomMeme"}

    @loader.command()
    async def meme(self, message):
        """Прислать случайный мем на русском"""
        await utils.answer(message, "🇷🇺 **Ищу годный мемас...**")
        
        try:
            async with aiohttp.ClientSession() as session:
                # Берем мемы из сабреддита r/Pikabu (там всё на русском)
                async with session.get("https://meme-api.com/gimme/Pikabu") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        meme_url = data.get("url")
                        title = data.get("title")
                        
                        await self._client.send_file(
                            message.peer_id, 
                            meme_url, 
                            caption=f"🔥 **{title}**\n\n📌 *Источник: r/Pikabu*"
                        )
                        await message.delete()
                    else:
                        await utils.answer(message, "❌ Не удалось найти русские мемы.")
        except Exception as e:
            logger.error(f"Meme error: {e}")
            await utils.answer(message, "❌ Ошибка при поиске мема.")