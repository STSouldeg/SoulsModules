# meta developer: @aethergeminibot, @Elizar_SoulsTeam
# requires: aiohttp

from .. import loader, utils
import aiohttp
import os
import time
import asyncio

@loader.tds
class UniversalLoadMultiMod(loader.Module):
    """Universal Downloader (Multi-Mirror): Скачивает видео через сеть зеркал Cobalt. Автоматический обход блокировок."""
    strings = {"name": "UniversalLoadMulti"}

    @loader.command()
    async def dl(self, message):
        """[ссылка] — Скачать видео (TikTok, Insta, YT) через рабочее зеркало"""
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

        status_msg = await utils.answer(message, f"📡 **Поиск рабочего зеркала...**\n`{url}`")
        
        # Список зеркал API (Cobalt Instances)
        api_instances = [
            "https://api.cobalt.tools/api/json",      # Official
            "https://co.wuk.sh/api/json",             # Popular Mirror
            "https://api.server.garden/api/json",     # Alternative
            "https://cobalt.api.wuk.koeln/api/json",  # Backup EU
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

        download_link = None
        working_api = None

        async with aiohttp.ClientSession() as session:
            # 1. Перебор зеркал
            for api_url in api_instances:
                try:
                    async with session.post(api_url, json=payload, headers=headers, timeout=10) as response:
                        if response.status == 200:
                            data = await response.json()
                            state = data.get("status")
                            
                            if state in ["redirect", "tunnel"]:
                                download_link = data.get("url")
                            elif state == "picker":
                                picker = data.get("picker")
                                if picker:
                                    download_link = picker[0].get("url")
                            
                            if download_link:
                                working_api = api_url
                                break # Нашли рабочее!
                except Exception:
                    continue # Пробуем следующее
            
            if not download_link:
                await utils.answer(status_msg, "❌ **Ошибка сети:** Ни одно зеркало не ответило.\nВозможно, хостинг блокирует внешние соединения.")
                return

            # 2. Скачивание
            await utils.answer(status_msg, f"⬇️ **Скачивание** (через {working_api.split('/')[2]})...")
            
            file_name = f"video_{int(time.time())}.mp4"
            
            try:
                async with session.get(download_link) as file_resp:
                    if file_resp.status == 200:
                        with open(file_name, 'wb') as f:
                            while True:
                                chunk = await file_resp.content.read(1024*1024)
                                if not chunk:
                                    break
                                f.write(chunk)
                    else:
                        await utils.answer(status_msg, "❌ Ошибка скачивания файла.")
                        return
            except Exception as e:
                await utils.answer(status_msg, f"❌ Ошибка сохранения: {e}")
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

        if 'file_name' in locals() and os.path.exists(file_name):
            os.remove(file_name)