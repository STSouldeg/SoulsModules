# meta developer: @aethergeminibot
from .. import loader, utils
import aiohttp
import logging

logger = logging.getLogger(__name__)

@loader.tds
class RandomParrotMod(loader.Module):
    """Модуль для генерации случайных попугаев (птиц)"""
    strings = {"name": "RandomParrot"}

    @loader.command()
    async def parrot(self, message):
        """Прислать фото случайного попугая/птицы"""
        await utils.answer(message, "🦜 **Ищу самого красивого попугая...**")
        
        try:
            async with aiohttp.ClientSession() as session:
                # Используем надежное API для птиц
                async with session.get("https://some-random-api.com/animal/bird") as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        image_url = data.get('image')
                        fact = data.get('fact', 'Просто красивый птиц!')
                        
                        await self._client.send_file(
                            message.peer_id, 
                            image_url, 
                            caption=f"🦜 **Твой попугай готов!**\n\n📖 *Факт:* {fact}"
                        )
                        await message.delete()
                    else:
                        await utils.answer(message, "❌ Не удалось найти попугая, попробуй позже.")
        except Exception as e:
            logger.error(f"Parrot error: {e}")
            await utils.answer(message, f"❌ Произошла ошибка: {str(e)}")