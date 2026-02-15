# meta developer: @aethergeminibot, @Elizar_SoulsTeam
# requires: aiohttp

from .. import loader, utils
import aiohttp
import os
import time
import json

@loader.tds
class UniversalLoadNuclearMod(loader.Module):
    """Universal Downloader (Nuclear): Обход сломанного DNS. Использует прямой IP-адресинг и DoH."""
    strings = {"name": "UniversalLoadNuclear"}

    async def resolve_doh(self, domain):
        """Резолвит домен через Google DNS-over-HTTPS, обходя системный DNS"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://dns.google/resolve?name={domain}&type=A"
                async with session.get(url, timeout=5) as response:
                    if response.status == 200:
                        data = await response.json()
                        if "Answer" in data:
                            return data["Answer"][0]["data"]
        except:
            pass
        return None

    @loader.command()
    async def dl(self, message):
        """[ссылка] — Скачать видео (TikTok, Insta, YT) в обход DNS"""
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
            await utils.answer(message, "❌ **Нет ссылки!**\nИспользуй: `.dl <ссылка>` или ответь на сообщение с ссылкой.")
            return

        status_msg = await utils.answer(message, f"☢️ **Nuclear Protocol:** Обход DNS...\n`{url}`")
        
        # Целевой домен API
        target_domain = "co.wuk.sh"
        # Резервный IP Cloudflare (если DoH не сработает)
        target_ip = "172.67.155.210" 

        # 1. Пытаемся узнать IP через Google
        resolved_ip = await self.resolve_doh(target_domain)
        if resolved_ip:
            target_ip = resolved_ip
            await utils.answer(status_msg, f"🔍 **DNS Bypassed:** IP найден: `{target_ip}`")
        else:
            await utils.answer(status_msg, f"⚠️ **DNS Fail:** Использую резервный IP `{target_ip}`")

        # Формируем "прямой" URL
        api_url = f"https://{target_ip}/api/json"
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Host": target_domain  # Важно! Подменяем хост для Cloudflare
        }
        
        payload = {
            "url": url,
            "vQuality": "720",
            "filenamePattern": "basic",
            "isAudioOnly": False
        }

        file_name = f"video_{int(time.time())}.mp4"

        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
                # 2. Запрос к API напрямую по IP
                async with session.post(api_url, json=payload, headers=headers, timeout=20) as response:
                    if response.status != 200:
                        await utils.answer(status_msg, f"❌ **Ошибка API:** Сервер {target_ip} вернул код {response.status}")
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
                        await utils.answer(status_msg, f"❌ **Ссылка не получена.**\nОтвет: {data}")
                        return

                # 3. Разбор ссылки для скачивания (нужно тоже обойти DNS если домен тот же)
                # Обычно ссылка ведет на тот же домен
                dl_domain = download_link.split('/')[2]
                dl_path = "/" + "/".join(download_link.split('/')[3:])
                
                # Если домен тот же, используем тот же IP
                if dl_domain == target_domain:
                    dl_url = f"https://{target_ip}{dl_path}"
                    dl_headers = {"Host": dl_domain}
                else:
                    # Если домен другой, пробуем зарезолвить его
                    dl_ip = await self.resolve_doh(dl_domain)
                    if dl_ip:
                         dl_url = f"https://{dl_ip}{dl_path}"
                         dl_headers = {"Host": dl_domain}
                    else:
                        # Если не вышло, пробуем как есть (авось сработает)
                        dl_url = download_link
                        dl_headers = {}

                await utils.answer(status_msg, "⬇️ **Скачивание файла** (Direct IP)...")
                
                async with session.get(dl_url, headers=dl_headers, timeout=60) as file_resp:
                    if file_resp.status == 200:
                        with open(file_name, 'wb') as f:
                            while True:
                                chunk = await file_resp.content.read(1024*1024)
                                if not chunk:
                                    break
                                f.write(chunk)
                    else:
                         await utils.answer(status_msg, f"❌ Ошибка скачивания: {file_resp.status}")
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
            
            if isinstance(status_msg, list):
                for m in status_msg: await m.delete()
            else:
                await status_msg.delete()

        except Exception as e:
            await utils.answer(status_msg, f"❌ **Nuclear Error:**\n`{str(e)}`")
        
        finally:
            if os.path.exists(file_name):
                os.remove(file_name)