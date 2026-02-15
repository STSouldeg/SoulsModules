# meta developer: @Elizar_SoulsTeam
import random
import aiohttp
import io
from .. import loader, utils

@loader.tds
class MCMobsMod(loader.Module):
    """Рандомные котики Minecraft (v14 - Wiki Mirror)"""
    strings = {"name": "MCMobs"}

    @loader.unrestricted
    @loader.command(ru_doc="Выдать фото котика из Minecraft")
    async def mcmobcmd(self, message):
        """Команда .mcmob"""
        # Используем ТОЛЬКО домен upload.wikimedia.org (он у тебя работает 100%)
        cats = [
            "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Tuxedo_Cat_JE2_BE2.png/600px-Tuxedo_Cat_JE2_BE2.png",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Tabby_Cat_JE2_BE2.png/600px-Tabby_Cat_JE2_BE2.png",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Ginger_Cat_JE2_BE2.png/600px-Ginger_Cat_JE2_BE2.png",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/White_Cat_JE2_BE2.png/600px-White_Cat_JE2_BE2.png",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Black_Cat_JE2_BE2.png/600px-Black_Cat_JE2_BE2.png",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/British_Shorthair_Cat_JE2_BE2.png/600px-British_Shorthair_Cat_JE2_BE2.png",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Calico_Cat_JE2_BE2.png/600px-Calico_Cat_JE2_BE2.png",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Persian_Cat_JE2_BE2.png/600px-Persian_Cat_JE2_BE2.png",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Ragdoll_Cat_JE2_BE2.png/600px-Ragdoll_Cat_JE2_BE2.png",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Siamese_Cat_JE2_BE2.png/600px-Siamese_Cat_JE2_BE2.png",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Jellie_Cat_JE2_BE2.png/600px-Jellie_Cat_JE2_BE2.png"
        ]
        
        message = await utils.answer(message, "🐈 `Котик заходит через Википедию...`")
        random.shuffle(cats)
        
        # Заголовки точно такие же, как в рабочем модуле с дельфинами
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

        async with aiohttp.ClientSession(headers=headers) as session:
            for url in cats:
                try:
                    async with session.get(url, timeout=10) as resp:
                        if resp.status == 200:
                            content = await resp.read()
                            image = io.BytesIO(content)
                            image.name = "cat.png"
                            await message.client.send_file(message.chat_id, image, reply_to=message.reply_to_msg_id)
                            await message.delete()
                            return
                except:
                    continue
        
        await utils.answer(message, "❌ Ошибка. Если дельфины работают, а это нет — попробуй .restart")