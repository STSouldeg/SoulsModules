
# meta developer: @aethergeminibot
from .. import loader, utils
import requests
import random
import io

class DolphinMod(loader.Module):
    """Модуль для вызова дельфинов (Stable Version)"""
    strings = {"name": "Dolphin"}

    @loader.command()
    async def dolphincmd(self, message):
        """Вызвать дельфина"""
        await utils.answer(message, "🐬 <i>Ищу дельфина в глубоких водах...</i>")
        
        # Используем LoremFlickr - он стабильнее для поиска по тегам
        url = f"https://loremflickr.com/1280/720/dolphin?random={random.randint(1, 9999)}"
        
        try:
            # Скачиваем в память, чтобы Telegram точно принял файл
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                img = io.BytesIO(response.content)
                img.name = "dolphin.jpg"
                await message.client.send_file(
                    message.chat_id, 
                    img, 
                    caption="🐬 <b>Дельфин успешно доставлен!</b>",
                    reply_to=message.reply_to_msg_id
                )
                await message.delete()
            else:
                raise Exception
        except Exception:
            # Резервная ссылка на статику, если сервис упал
            backup = "https://images.unsplash.com/photo-1570481662006-a3a1374699e8?w=800"
            await message.client.send_file(message.chat_id, backup, caption="🐬 <b>Дельфин из резервного фонда!</b>")
            await message.delete()