# meta developer: @aethergeminibot, @Elizar_SoulsTeam
# requires: yt-dlp

from .. import loader, utils
import os
import time
import sys
import subprocess
import logging

logger = logging.getLogger(__name__)

@loader.tds
class UniversalLoadMod(loader.Module):
    """Universal Downloader: Скачивает видео с TikTok, Instagram, YouTube, Pinterest без водяных знаков."""
    strings = {"name": "UniversalLoad"}

    @loader.command()
    async def dl(self, message):
        """[ссылка] — Скачать видео (TikTok, Insta, YouTube, etc.)"""
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

        status_msg = await utils.answer(message, f"📥 **Загрузка...**\n`{url}`")
        
        # --- БЛОК ПРИНУДИТЕЛЬНОЙ УСТАНОВКИ ---
        try:
            import yt_dlp
        except ImportError:
            await utils.answer(status_msg, "🔨 **Первый запуск: Установка библиотек...**\nЭто займет 10-20 секунд.")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
                import yt_dlp
            except Exception as e:
                await utils.answer(status_msg, f"❌ **Ошибка установки:** Хостинг запрещает установку модулей.\nОшибка: `{e}`")
                return
        # -------------------------------------

        timestamp = int(time.time())
        file_path_base = f"download_{timestamp}"
        
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f"{file_path_base}.%(ext)s",
            'noplaylist': True,
            'quiet': True,
            'max_filesize': 500 * 1024 * 1024,
            'geo_bypass': True,
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        downloaded_file = None

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'Video')
                uploader = info.get('uploader', 'Unknown')
                
                ext = info.get('ext', 'mp4')
                downloaded_file = f"{file_path_base}.{ext}"
                
                if not os.path.exists(downloaded_file):
                    downloaded_file = ydl.prepare_filename(info)

                caption = f"📹 **{title}**\n👤 **{uploader}**\n\n📥 *Downloaded via @Elizar_SoulsTeam*"

                await utils.answer(status_msg, "📤 **Отправка...**")
                
                await self._client.send_file(
                    message.peer_id,
                    downloaded_file,
                    caption=caption,
                    supports_streaming=True,
                    reply_to=reply.id if reply else message.id
                )
                
                if isinstance(status_msg, list):
                    for m in status_msg: await m.delete()
                else:
                    await status_msg.delete()

        except Exception as e:
            await utils.answer(status_msg, f"❌ **Ошибка:**\n`{str(e)}`")
        
        finally:
            if downloaded_file and os.path.exists(downloaded_file):
                os.remove(downloaded_file)