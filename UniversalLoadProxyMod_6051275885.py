# meta developer: @aethergeminibot, @Elizar_SoulsTeam
# requires: aiohttp

from .. import loader, utils
import aiohttp
import os
import time
import urllib.parse
import json

@loader.tds
class UniversalLoadProxyMod(loader.Module):
    """Universal Downloader (Proxy): Использует веб-прокси для обхода тотальных блокировок сети и DNS."""
    strings = {"name": "UniversalLoadProxy"}

    @loader.command()
    async def dl(self, message):
        """[ссылка] — Скачать видео через веб-прокси"""
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

        status_msg = await utils.answer(message, f"⛓ **Proxy Tunnel:** Подключение...\n`{url}`")
        
        # Целевой API
        target_api = "https://api.cobalt.tools/api/json"
        
        # Прокси-сервис (CorsProxy.io)
        # Он пересылает наш запрос к целевому API
        proxy_url = f"https://corsproxy.io/?{urllib.parse.quote(target_api)}"
        
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

        try:
            async with aiohttp.ClientSession() as session:
                # 1. Запрос к API через Прокси
                # Мы отправляем POST на адрес ПРОКСИ, он перешлет его на Cobalt
                async with session.post(proxy_url, json=payload, headers=headers, timeout=20) as response:
                    if response.status != 200:
                        # Если первый прокси не сработал, пробуем резервный API напрямую через другой прокси
                        # (резервный вариант добавим если этот не сработает)
                        err_text = await response.text()
                        await utils.answer(status_msg, f"❌ **Proxy Error:** {response.status}\n`{err_text[:100]}`")
                        return
                    
                    data = await response.json()
                    
                    state = data.get("status")
                    download_link = None
                    if state in ["redirect", "tunnel"]:
                        download_link = data.get("url")
                    elif state == "picker":
                        picker = data.get("picker")
                        if picker:
                            download_link = picker[0].get("url")
                    
                    if not download_link:
                        await utils.answer(status_msg, f"❌ **API Error:** Ссылка не получена.\nОтвет: `{data}`")
                        return

                # 2. Скачивание файла (Тоже через прокси, если прямая ссылка не работает)
                # Сначала пробуем напрямую (иногда ссылки на CDN работают лучше API)
                await utils.answer(status_msg, "⬇️ **Скачивание файла...**")
                
                # Функция для скачивания
                async def download_file(link, use_proxy=False):
                    target = f"https://corsproxy.io/?{urllib.parse.quote(link)}" if use_proxy else link
                    async with session.get(target, timeout=60) as r:
                        if r.status == 200:
                            with open(file_name, 'wb') as f:
                                while True:
                                    chunk = await r.content.read(1024*1024)
                                    if not chunk: break
                                    f.write(chunk)
                            return True
                        return False

                # Пробуем скачать напрямую
                if not await download_file(download_link, use_proxy=False):
                    await utils.answer(status_msg, "⚠️ Прямое скачивание не удалось, пробую через тоннель...")
                    # Если не вышло — пробуем через прокси
                    if not await download_file(download_link, use_proxy=True):
                        await utils.answer(status_msg, "❌ **Download Error:** Не удалось скачать файл даже через прокси.")
                        return

            # 3. Отправка
            await utils.answer(status_msg, "📤 **Отправка...**")
            caption = f"📹 **Video**\n📥 *Via @Elizar_SoulsTeam*"
            
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
            await utils.answer(status_msg, f"❌ **Critical Proxy Error:**\n`{str(e)}`")
        
        finally:
            if os.path.exists(file_name):
                os.remove(file_name)