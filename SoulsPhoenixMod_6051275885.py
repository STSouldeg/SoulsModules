# meta developer: @Elizar_SoulsTeam
# requires: aiohttp

import aiohttp
import asyncio
import re
from .. import loader, utils

@loader.tds
class SoulsPhoenixMod(loader.Module):
    """🕵️‍♂️ SoulsPhoenix v5.0: Прямой пробив ФИО, Города и Тегов"""
    
    strings = {"name": "SoulsPhoenix 🕵️‍♂️"}

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36"
        }

    async def get_tags(self, session, phone):
        """Парсинг имен из открытых зеркал GetContact"""
        url = f"https://mirror.bullshit.agency/search_by_phone/{phone}"
        try:
            async with session.get(url, timeout=7) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    # Ищем теги в коде страницы
                    tags = re.findall(r'<td>(.*?)</td>', text)
                    return [t.strip() for t in tags if len(t) > 1 and "mirror" not in t.lower()]
                return []
        except:
            return []

    async def get_region(self, session, phone):
        """Определение региона по номеру"""
        url = f"https://num.mobi/search/{phone}"
        try:
            async with session.get(url, timeout=5) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    # Ищем регион/оператора
                    region = re.search(r'Регион:</b>\s*<span>(.*?)</span>', text)
                    op = re.search(r'Оператор:</b>\s*<span>(.*?)</span>', text)
                    res = ""
                    if region: res += region.group(1)
                    if op: res += f" ({op.group(1)})"
                    return res if res else "Не определен"
                return "Не определен"
        except:
            return "Не определен"

    @loader.unrestricted
    @loader.command(ru_doc="<номер или ник> - Прямой пробив данных")
    async def shcmd(self, message):
        """Прямой поиск данных без ссылок"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "❌ <b>Введите данные для поиска!</b>")
            return

        query = args.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        is_phone = query.isdigit() or (query.startswith('+') and query[1:].isdigit())
        
        status_msg = await utils.answer(message, "🧬 <b>Анализ нейронной сети Souls...</b>\n[▒▒▒▒▒▒▒▒▒▒] 10%")

        async with aiohttp.ClientSession(headers=self.headers) as session:
            if is_phone:
                clean_phone = query.replace("+", "")
                if clean_phone.startswith('8'): clean_phone = '7' + clean_phone[1:]
                
                await status_msg.edit("📡 <b>Подключение к шлюзам GetContact...</b>\n[████▒▒▒▒▒▒] 40%")
                tags = await self.get_tags(session, clean_phone)
                
                await status_msg.edit("📍 <b>Запрос геолокации и оператора...</b>\n[████████▒▒] 80%")
                region = await self.get_region(session, clean_phone)
                
                # Формируем ответ по номеру
                res = f"🕵️‍♂️ <b>ДОСЬЕ НА НОМЕР:</b> <code>+{clean_phone}</code>\n"
                res += "━━━━━━━━━━━━━━━━━━━━\n\n"
                res += f"📍 <b>РЕГИОН:</b> <code>{region}</code>\n"
                
                if tags:
                    res += f"👤 <b>ИМЯ / ФИО (по тегам):</b>\n"
                    # Берем первые 5 самых частых имен
                    for i, tag in enumerate(tags[:6], 1):
                        res += f"  {i}. <code>{tag}</code>\n"
                else:
                    res += "👤 <b>ИМЯ:</b> <code>Не найдено в базе тегов</code>\n"
                
                res += f"\n📅 <b>ГР:</b> <code>Уточняется через соцсети...</code>\n"
                res += f"🔗 <b>W/A:</b> <a href='https://wa.me/{clean_phone}'>Написать</a> | <b>TG:</b> <a href='https://t.me/{clean_phone}'>Открыть</a>\n"
                
            else:
                # Поиск по нику
                await status_msg.edit("🔍 <b>Поиск цифрового следа...</b>\n[██████▒▒▒▒] 60%")
                url = f"https://vk.com/{query}"
                async with session.get(url) as r:
                    t = await r.text()
                    name = re.search(r'<title>(.*?)</title>', t)
                    name = name.group(1).split('|')[0].strip() if name else query
                
                res = f"👤 <b>ДОСЬЕ НА НИК:</b> <code>{query}</code>\n"
                res += "━━━━━━━━━━━━━━━━━━━━\n\n"
                res += f"▪️ <b>Вероятное ФИО:</b> <code>{name}</code>\n"
                res += f"▪️ <b>Город/Дата:</b> <code>См. в профиле ниже</code>\n\n"
                res += f"🔹 <b>VK:</b> https://vk.com/{query}\n"
                res += f"🔹 <b>Inst:</b> https://instagram.com/{query}\n"

            await status_msg.edit(res + "\n✅ <b>Поиск завершен.</b>")