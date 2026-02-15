# meta developer: @aethergeminibot, @Elizar_SoulsTeam
# requires: aiohttp

from .. import loader, utils
import aiohttp
import os
import time

@loader.tds
class UniversalLoadApiMod(loader.Module):
    """Universal Downloader (API): Скачивает видео через внешний сервис. Работает даже если IP хостинга в бане."""
    strings = {"name": "UniversalLoadAPI"}

    @loader.command()
    async def dl(self, message):
        """[ссылка] — Скачать видео (TikTok, Insta, YT) через API"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        url = None
        if args:
            url = args.strip()
        elif reply:
            if reply.text:
                for word in reply.text.split():
                    if word.startswith(("http://", "https://")):
                        url = word
                        break
            if not url and reply.buttons:
                 for row in reply.buttons:
                    for btn in row:
                        if hasattr(btn, 'url') and btn.url:
                            url = btn.url
                            break
        
        if not url:
            await utils.answer(message, "❌ **Нет ссылки!**")
            return

        status_msg = await utils.answer(message, f"🔄 **Обработка через API...**\n`{url}`")
        
        # API Cobalt (один из лучших публичных инстансов)
        api_url = "https://api.cobalt.tools/api/json"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        payload = {
            "url": url,
            "vQuality": "720",
            "filenamePattern": "basic",
            "isAudioOnly": False
        }

        try:
            async with aiohttp.ClientSession() as session:
                # 1. Запрос к API
                async with session.post(api_url, json=payload, headers=headers) as response:
                    if response.status != 200:
                        text = await response.text()
                        # Попробуем резервный API, если основной лежит
                        api_url_backup = "https://co.wuk.sh/api/json"
                        async with session.post(api_url_backup, json=payload, headers=headers) as resp2:
                            if resp2.status != 200:
                                await utils.answer(status_msg, f"❌ **Ошибка API:** Сервер вернул код {resp2.status}")
                                return
                            data = await resp2.json()
                    else:
                        data = await response.json()

                # 2. Обработка ответа
                state = data.get("status")
                download_link = None
                
                if state == "redirect" or state == "tunnel":
                    download_link = data.get("url")
                elif state == "picker":
                    # Если это галерея фото/видео, берем первое
                    picker = data.get("picker")
                    if picker:
                        download_link = picker[0].get("url")
                
                if not download_link:
                    await utils.answer(status_msg, f"❌ **Не удалось получить ссылку.**\nОтвет API: `{data}`")
                    return

                # 3. Скачивание файла
                await utils.answer(status_msg, "⬇️ **Скачивание файла...**")
                
                file_name = f"video_{int(time.time())}.mp4"
                
                async with session.get(download_link) as file_resp:
                    if file_resp.status == 200:
                        with open(file_name, 'wb') as f:
                            while True:
                                chunk = await file_resp.content.read(1024*1024) # 1MB chunks
                                if not chunk:
                                    break
                                f.write(chunk)
                    else:
                        await utils.answer(status_msg, "❌ Ошибка при скачивании файла.")
                        return

                # 4. Отправка
                await utils.answer(status_msg, "📤 **Отправка...**")
                
                caption = f"📹 **Video**\n📥 *Via @Elizar_SoulsTeam*"
                
                await self._client.send_file(
                    message.peer_id,
                    file_name,
                    caption=caption,
                    supports_streaming=True,
                    reply_to=reply.id if reply else message.id
                )
                
                # Удаляем сообщение статуса
                if isinstance(status_msg, list):
                    for m in status_msg: await m.delete()
                else:
                    await status_msg.delete()

        except Exception as e:
            await utils.answer(status_msg, f"❌ **Критическая ошибка:**\n`{str(e)}`")
        
        finally:
            if 'file_name' in locals() and os.path.exists(file_name):
                os.remove(file_name)