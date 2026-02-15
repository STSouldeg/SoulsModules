# meta developer: @Elizar_SoulsTeam

import os
import random
import subprocess
import shutil
from .. import loader, utils

@loader.tds
class SoulsAnimalsMod(loader.Module):
    """🐧 SoulsAnimals v44 (Linux Shell)"""
    
    strings = {"name": "SoulsAnimals 🐾"}

    def __init__(self):
        self.cat_urls = [
            "https://static.wikia.nocookie.net/minecraft_gamepedia/images/0/04/Tuxedo_Cat_JE2_BE2.png",
            "https://static.wikia.nocookie.net/minecraft_gamepedia/images/7/77/Red_Cat_JE2_BE2.png",
            "https://static.wikia.nocookie.net/minecraft_gamepedia/images/5/5e/Siamese_Cat_JE2_BE2.png",
            "https://static.wikia.nocookie.net/minecraft_gamepedia/images/a/a6/All_Black_Cat_JE1_BE1.png",
            "https://static.wikia.nocookie.net/minecraft_gamepedia/images/b/b7/Tabby_Cat_JE2_BE2.png",
            # Резервные стабильные ссылки
            "https://raw.githubusercontent.com/PrismarineJS/minecraft-assets/master/data/1.16.4/entity/cat/black.png",
            "https://raw.githubusercontent.com/PrismarineJS/minecraft-assets/master/data/1.16.4/entity/cat/british_shorthair.png",
            "https://raw.githubusercontent.com/PrismarineJS/minecraft-assets/master/data/1.16.4/entity/cat/calico.png"
        ]
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

    @loader.unrestricted
    @loader.command(ru_doc="🐬 Дельфин")
    async def dolphincmd(self, message):
        """Фото дельфина"""
        url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Tursiops_truncatus_01.jpg/800px-Tursiops_truncatus_01.jpg"
        await self._sys_download_send(message, url, "dolphin.jpg")

    @loader.unrestricted
    @loader.command(ru_doc="🐈 Рандомный кот (System)")
    async def mcmobcmd(self, message):
        """Случайный кот (через curl/wget)"""
        url = random.choice(self.cat_urls)
        await self._sys_download_send(message, url, "cat.png")

    async def _sys_download_send(self, message, url, filename):
        temp_file = f"temp_{random.randint(1000, 9999)}_{filename}"
        
        # Определяем, чем качать
        has_curl = shutil.which("curl") is not None
        has_wget = shutil.which("wget") is not None
        
        command = []
        
        if has_curl:
            # curl -L (follow redirects) -A "User-Agent" -o filename url
            command = ["curl", "-L", "-A", self.user_agent, "-o", temp_file, url]
        elif has_wget:
            # wget -U "User-Agent" -O filename url
            command = ["wget", "-U", self.user_agent, "-O", temp_file, url]
        else:
            await utils.answer(message, "🚫 <b>Ошибка:</b> На сервере нет ни curl, ни wget.")
            return

        try:
            # Запускаем системную команду
            # Используем run_sync, чтобы не фризить бота во время скачивания
            await utils.run_sync(subprocess.run, command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Проверяем, скачался ли файл и не пустой ли он
            if os.path.exists(temp_file) and os.path.getsize(temp_file) > 0:
                await self.client.send_file(
                    message.chat_id,
                    temp_file,
                    reply_to=message.reply_to_msg_id
                )
                await message.delete()
            else:
                await utils.answer(message, "💢 <b>Ошибка:</b> Файл скачался пустым (0 байт). Возможно, ссылка битая.")

        except subprocess.CalledProcessError:
            await utils.answer(message, "❌ <b>Ошибка:</b> Системная команда вернула код ошибки (Download failed).")
        except Exception as e:
            await utils.answer(message, f"☠️ <b>Critical:</b> {e}")
        
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)