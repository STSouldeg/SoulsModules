# meta developer: @aethergeminibot, @Elizar_SoulsTeam
# requires: aiohttp

from .. import loader, utils
import aiohttp
import os
import time

@loader.tds
class UniversalLoadTikWMMod(loader.Module):
    """Universal Downloader (TikWM): Альтернативный загрузчик для TikTok, если Cobalt заблокирован."""
    strings = {"name": "UniversalLoadTikWM"}

    @loader.command()
    async def dl(self, message):
        """[ссылка] — Скачать TikTok через TikWM (резервный метод)"""
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
        
        if not url:
            await utils.answer(message, "❌ **Нет ссылки!**")
            return

        status_msg = await utils.answer(message, f"🐉 **TikWM Protocol:** Подключение...\n`{url}`")
        
        # TikWM API Endpoint
        api_url = "https://www.tikwm.com/api/"
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
        }
        
        # TikWM принимает данные в form-data или query params
        params = {
            "url": url,
            "count": 12,
            "cursor": 0,
            "web": 1,
            "hd": 1
        }

        file_name = f"video_{int(time.time())}.mp4"

        try:
            async with aiohttp.ClientSession() as session:
                # 1. Запрос к API
                async with session.post(api_url, data=params, headers=headers, timeout=20) as response:
                    if response.status != 200:
                        await utils.answer(status_msg, f"❌ **TikWM Error:** API вернул {response.status}")
                        return
                    
                    data = await response.json()
                    
                    if data.get("code") != 0:
                        msg = data.get("msg", "Unknown Error")
                        await utils.answer(status_msg, f"❌ **API Error:** {msg}")
                        return
                    
                    video_data = data.get("data", {})
                    # Пробуем HD ссылку, если нет — обычную
                    download_link = video_data.get("hdplay") or video_data.get("play")
                    
                    if not download_link:
                         await utils.answer(status_msg, f"❌ **Link Error:** Видео не найдено в ответе API.")
                         return
                    
                    # Если ссылка относительная (начинается с /), добавляем домен
                    if download_link.startswith("/"):
                        download_link = "https://www.tikwm.com" + download_link

                # 2. Скачивание файла
                await utils.answer(status_msg, "⬇️ **Скачивание файла** (TikWM CDN)...")
                
                async with session.get(download_link, headers=headers, timeout=60) as file_resp:
                    if file_resp.status == 200:
                        with open(file_name, 'wb') as f:
                            while True:
                                chunk = await file_resp.content.read(1024*1024)
                                if not chunk:
                                    break
                                f.write(chunk)
                    else:
                         await utils.answer(status_msg, f"❌ Ошибка скачивания файла: {file_resp.status}")
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
            await utils.answer(status_msg, f"❌ **Error:** `{str(e)}`")
        
        finally:
            if os.path.exists(file_name):
                os.remove(file_name)