# meta developer: @aethergeminibot
from .. import loader, utils
import os
import requests
import urllib.parse
import logging

logger = logging.getLogger(__name__)

@loader.tds
class MusicSearchMod(loader.Module):
    """Модуль для поиска и скачивания музыки"""
    strings = {"name": "MusicSearch"}

    @loader.command()
    async def song(self, message):
        """<название> - Найти и скачать музыку"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "❌ Введи название песни!")
            return

        await utils.answer(message, f"🔍 **Ищу: {args}...**")
        
        try:
            # Используем публичный инстанс API для поиска и загрузки с YouTube
            # Это позволяет не нагружать сервер тяжелыми библиотеками
            search_query = urllib.parse.quote(args)
            api_url = f"https://api.vkr.com.ua/youtube/search.php?v={search_query}"
            
            response = requests.get(api_url).json()
            
            if "items" in response and len(response["items"]) > 0:
                video_id = response["items"][0]["id"]
                video_title = response["items"][0]["title"]
                
                # Получаем прямую ссылку на скачивание (через сторонний сервис для легкости модуля)
                download_url = f"https://api.vkr.com.ua/youtube/get.php?video=https://www.youtube.com/watch?v={video_id}&type=audio"
                
                await utils.answer(message, f"📥 **Загружаю: {video_title}...**")
                
                # Отправляем файл
                await self._client.send_file(
                    message.peer_id, 
                    download_url, 
                    caption=f"🎵 **Найдено:** {video_title}",
                    attributes=[{"_": "DocumentAttributeAudio", "title": video_title, "performer": "YouTube Search"}]
                )
                await message.delete()
            else:
                await utils.answer(message, "❌ Ничего не найдено.")
                
        except Exception as e:
            logger.error(f"Music error: {e}")
            await utils.answer(message, "❌ Произошла ошибка при поиске. Попробуй другое название.")