# meta developer: @aethergeminibot, @Elizar_SoulsTeam
# requires: aiohttp

from .. import loader, utils
import aiohttp
import os
import time
import logging

logger = logging.getLogger(__name__)

@loader.tds
class UniversalLoadUltraMod(loader.Module):
    """Universal Downloader (Ultra): Агрессивный перебор зеркал. Скачивает видео, игнорируя ошибки DNS и блокировки."""
    strings = {"name": "UniversalLoadUltra"}

    @loader.command()
    async def dl(self, message):
        """[ссылка] — Скачать видео (TikTok, Insta, YT) методом перебора"""
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

        status_msg = await utils.answer(message, f"🛡 **Запуск Ultra-протокола...**\n`{url}`")
        
        # Расширенный список зеркал
        api_instances = [
            "https://api.cobalt.tools/api/json",      # Official
            "https://co.wuk.sh/api/json",             # Popular
            "https://api.server.garden/api/json",     # Backup 1
            "https://cobalt.api.wuk.koeln/api/json",  # Backup 2
            "https://api.chrunos.com/api/json",       # Backup 3
            "https://dl.khub.ky/api/json",            # Backup 4
        ]

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        
        payload = {
            "url": url,
            "vQuality": "720",
            "filenamePattern": "basic",
            "isAudioOnly": False
        }

        file_name = f"video_{int(time.time())}.mp4"
        success = False
        last_error = ""

        async with aiohttp.ClientSession() as session:
            for i, api_url in enumerate(api_instances):
                mirror_name = api_url.split('/')[2]
                await utils.answer(status_msg, f"📡 **Зеркало {i+1}/{len(api_instances)}:** `{mirror_name}`...")
                
                try:
                    # 1. Запрос к API
                    async with session.post(api_url, json=payload, headers=headers, timeout=15) as response:
                        if response.status != 200:
                            last_error = f"API Error {response.status}"
                            continue # Следующее зеркало
                        
                        data = await response.json()
                        
                        # Парсинг ссылки
                        download_link = None
                        state = data.get("status")
                        if state in ["redirect", "tunnel"]:
                            download_link = data.get("url")
                        elif state == "picker":
                            picker = data.get("picker")
                            if picker:
                                download_link = picker[0].get("url")
                        
                        if not download_link:
                            last_error = "No link in response"
                            continue

                    # 2. Попытка скачивания (Сразу же, чтобы проверить доступность файла)
                    await utils.answer(status_msg, f"⬇️ **Скачивание файла** (через {mirror_name})...")
                    
                    async with session.get(download_link, timeout=60) as file_resp:
                        if file_resp.status == 200:
                            with open(file_name, 'wb') as f:
                                while True:
                                    chunk = await file_resp.content.read(1024*1024)
                                    if not chunk:
                                        break
                                    f.write(chunk)
                            
                            # Проверка, что файл не пустой
                            if os.path.getsize(file_name) > 0:
                                success = True
                                break # ВЫХОДИМ ИЗ ЦИКЛА, ВСЁ ПОЛУЧИЛОСЬ
                            else:
                                last_error = "Empty file received"
                        else:
                            last_error = f"Download Error {file_resp.status}"

                except Exception as e:
                    last_error = str(e)
                    logger.error(f"Mirror {mirror_name} failed: {e}")
                    continue

            if not success:
                await utils.answer(status_msg, f"❌ **Не удалось скачать видео.**\nВсе зеркала недоступны или заблокированы.\nПоследняя ошибка: `{last_error}`")
                if os.path.exists(file_name):
                    os.remove(file_name)
                return

            # 3. Отправка
            await utils.answer(status_msg, "📤 **Отправка...**")
            caption = f"📹 **Video**\n📥 *Via @Elizar_SoulsTeam*"
            
            try:
                await self._client.send_file(
                    message.peer_id,
                    file_name,
                    caption=caption,
                    supports_streaming=True,
                    reply_to=reply.id if reply else message.id
                )
                if isinstance(status_msg, list):
                    for m in status_msg: await m.delete()
                else:
                    await status_msg.delete()
            except Exception as e:
                 await utils.answer(status_msg, f"❌ Ошибка отправки в Telegram: {e}")
            
            finally:
                if os.path.exists(file_name):
                    os.remove(file_name)