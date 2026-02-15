# meta developer: @Elizar_SoulsTeam
# scope: hikka_only

import random
import aiohttp
import io
import ssl
from .. import loader, utils

@loader.tds
class MinecraftMobsMod(loader.Module):
    """Самая стабильная версия Minecraft Mobs"""
    
    strings = {
        "name": "MinecraftMobs",
        "loading": "<b>[MC] Загрузка моба...</b>",
        "error": "<b>[MC] Не удалось призывать моба. Попробуй еще раз.</b>"
    }

    def __init__(self):
        # Используем ссылки на файлы, которые реже блокируют
        self.mobs = [
            {"name": "Крипер", "url": "https://minecraft.wiki/images/Creeper_JE2_BE1.png"},
            {"name": "Зомби", "url": "https://minecraft.wiki/images/Zombie_JE3_BE2.png"},
            {"name": "Эндермен", "url": "https://minecraft.wiki/images/Enderman_JE3_BE2.png"},
            {"name": "Скелет", "url": "https://minecraft.wiki/images/Skeleton_JE3_BE2.png"},
            {"name": "Свинья", "url": "https://minecraft.wiki/images/Pig_JE3_BE2.png"},
            {"name": "Паук", "url": "https://minecraft.wiki/images/Spider_JE3_BE3.png"},
            {"name": "Странствующий торговец", "url": "https://minecraft.wiki/images/Wandering_Trader_JE2_BE2.png"},
            {"name": "Железный голем", "url": "https://minecraft.wiki/images/Iron_Golem_JE2_BE2.png"}
        ]

    async def mcmobcmd(self, message):
        """Показать случайного моба"""
        message = await utils.answer(message, self.strings("loading"))
        mob = random.choice(self.mobs)
        
        # Заголовки, чтобы сайт думал, что мы — обычный человек с браузером Chrome
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }

        try:
            # Отключаем проверку SSL, чтобы избежать ошибок в Termux/на старых серверах
            connector = aiohttp.TCPConnector(ssl=False)
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(mob['url'], headers=headers, timeout=20) as resp:
                    if resp.status == 200:
                        content = await resp.read()
                        img = io.BytesIO(content)
                        img.name = "mob.png"
                        
                        caption = f"👾 <b>Моб:</b> <code>{mob['name']}</code>"
                        await self._client.send_file(message.peer_id, img, caption=caption)
                        
                        if message.out:
                            await message.delete()
                    else:
                        await utils.answer(message, f"<b>[MC] Ошибка сайта: {resp.status}</b>")
        except Exception as e:
            await utils.answer(message, f"<b>[MC] Ошибка:</b> <code>{str(e)}</code>")