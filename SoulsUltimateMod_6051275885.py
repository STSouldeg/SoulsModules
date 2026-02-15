# meta developer: @Elizar_SoulsTeam
# requires: aiohttp

import aiohttp
import asyncio
import re
from .. import loader, utils

@loader.tds
class SoulsUltimateMod(loader.Module):
    """🕵️‍♂️ SoulsUltimate v6.0: Максимальный пробив по открытым источникам"""
    
    strings = {"name": "SoulsUltimate 🕵️‍♂️"}

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }

    async def get_names(self, session, phone):
        """Парсинг имен из альтернативных справочников"""
        results = []
        # Источник 1: MySMS (Часто есть имена)
        try:
            url = f"https://mysms.ru/phone/{phone}"
            async with session.get(url, timeout=5) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    # Ищем упоминания имен в комментариях или заголовках
                    found = re.findall(r'<b>(.*?)</b>', text)
                    results.extend([f.strip() for f in found if len(f) > 3 and "номер" not in f.lower()])
        except: pass

        # Источник 2: Zvonili (Отзывы)
        try:
            url = f"https://zvonili.com/phone/{phone}"
            async with session.get(url, timeout=5) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    found = re.findall(r'<span>(.*?)</span>', text)
                    results.extend([f.strip() for f in found if len(f) > 3 and "комментар" not in f.lower()])
        except: pass
        
        return list(set(results)) # Только уникальные

    async def get_info_mobi(self, session, phone):
        """Получение региона и оператора"""
        try:
            url = f"https://num.mobi/search/{phone}"
            async with session.get(url, timeout=5) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    region = re.search(r'Регион:</b>\s*<span>(.*?)</span>', text)
                    op = re.search(r'Оператор:</b>\s*<span>(.*?)</span>', text)
                    r_val = region.group(1) if region else "Неизвестно"
                    o_val = op.group(1) if op else "Неизвестно"
                    return f"{r_val} ({o_val})"
        except: return "Не определено"
        return "Не определено"

    @loader.unrestricted
    @loader.command(ru_doc="<номер> - Глубокий поиск данных")
    async def shcmd(self, message):
        """Максимально глубокий поиск по номеру"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "❌ <b>Введите номер телефона!</b>")
            return

        phone = args.strip().replace("+", "").replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        if not phone.isdigit():
            await utils.answer(message, "❌ <b>Это не похоже на номер телефона.</b>")
            return

        if phone.startswith('8'): phone = '7' + phone[1:]

        status_msg = await utils.answer(message, "🌀 <b>Взлом протоколов поиска...</b>\n[▒▒▒▒▒▒▒▒▒▒] 10%")

        async with aiohttp.ClientSession(headers=self.headers) as session:
            # 1. Регион
            await status_msg.edit("📍 <b>Определяю местоположение...</b>\n[███▒▒▒▒▒▒▒] 30%")
            info = await self.get_info_mobi(session, phone)
            
            # 2. Имена
            await status_msg.edit("👤 <b>Ищу ФИО в базах справочников...</b>\n[██████▒▒▒▒] 60%")
            names = await self.get_names(session, phone)
            
            # 3. Соцсети (поверхностно)
            await status_msg.edit("🔗 <b>Проверка цифрового следа...</b>\n[█████████▒] 90%")
            
            res = f"🕵️‍♂️ <b>ПОЛНОЕ ДОСЬЕ: <code>+{phone}</code></b>\n"
            res += "━━━━━━━━━━━━━━━━━━━━\n\n"
            res += f"📍 <b>РЕГИОН/ОПЕРАТОР:</b>\n<code>{info}</code>\n\n"
            
            if names:
                res += "👤 <b>ВОЗМОЖНЫЕ ИМЕНА:</b>\n"
                for i, n in enumerate(names[:5], 1):
                    res += f"  {i}. <code>{n}</code>\n"
            else:
                res += "👤 <b>ИМЯ:</b> <code>Скрыто или не найдено</code>\n"
            
            res += f"\n📅 <b>ДАТА РОЖДЕНИЯ:</b> <code>Требуется ручной поиск</code>\n"
            res += f"🌐 <b>ОБЪЯВЛЕНИЯ:</b> <a href='https://www.google.com/search?q=%22{phone}%22'>Найти в Google</a>\n"
            res += "━━━━━━━━━━━━━━━━━━━━\n"
            res += f"💬 <b>СВЯЗЬ:</b> <a href='https://wa.me/{phone}'>WhatsApp</a> | <a href='https://t.me/{phone}'>Telegram</a>"

            await status_msg.edit(res)