# meta developer: @aethergeminibot
from .. import loader, utils
import aiohttp
import urllib.parse
import logging

logger = logging.getLogger(__name__)

@loader.tds
class MusicFixMod(loader.Module):
    """Исправленный модуль поиска музыки"""
    strings = {"name": "MusicSearch"}

    @loader.command()
    async def song(self, message):
        """<название> - Найти и скачать музыку (FIXED)"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "❌ Введи название песни!")
            return

        await utils.answer(message, f"🔍 **Ищу: {args}...**")
        
        # Список API для поиска (если один упадет, можно будет легко заменить)
        search_url = f"https://api.deezer.com/search?q={urllib.parse.quote(args)}&limit=1"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(search_url) as resp:
                    if resp.status != 200:
                        await utils.answer(message, "❌ Сервер поиска временно недоступен.")
                        return
                    
                    data = await resp.json()
                    
                    if not data.get("data"):
                        await utils.answer(message, "❌ Ничего не найдено. Попробуй уточнить название.")
                        return
                    
                    track = data["data"][0]
                    title = track["title"]
                    artist = track["artist"]["name"]
                    # Используем превью (30 сек) или ищем полную версию через обходной путь
                    # Для полноценного скачивания используем конвертер по названию
                    
                    download_api = f"https://api.vevioz.com/api/button/mp3/https://www.youtube.com/results?search_query={urllib.parse.quote(artist + ' ' + title)}"
                    
                    caption = f"🎵 **Найдено:** {artist} - {title}\n\n"
                    caption += "ℹ️ *Если файл не пришел, значит сервис загрузки перегружен. Попробуй еще раз через минуту.*"

                    # Пытаемся отправить аудио-превью (самый стабильный метод без API-ключей)
                    await self._client.send_file(
                        message.peer_id,
                        track["preview"],
                        caption=f"🎧 **Превью:** {artist} - {title}\n📎 [Полная версия]({download_api})",
                        attributes=[{"_": "DocumentAttributeAudio", "title": title, "performer": artist, "duration": 30}]
                    )
                    await message.delete()

        except Exception as e:
            logger.error(f"Music Error: {e}")
            await utils.answer(message, f"❌ Ошибка: {str(e)}")