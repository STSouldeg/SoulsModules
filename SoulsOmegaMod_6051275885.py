# meta developer: @Elizar_SoulsTeam
# requires: aiohttp

import aiohttp
import asyncio
import re
from .. import loader, utils

@loader.tds
class SoulsOmegaMod(loader.Module):
    """🕵️‍♂️ SoulsOmega v8.0: Глубокий анализ номера (Регион, Имена, Мессенджеры)"""
    
    strings = {"name": "SoulsOmega 🕵️‍♂️"}

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }

    async def get_region(self, session, phone):
        """Определение региона и оператора"""
        try:
            url = f"https://rosreestr.subnets.ru/api.php?p={phone}"
            async with session.get(url, timeout=5) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return f"{data.get('region', 'Неизвестно')} ({data.get('operator', 'Неизвестно')})"
        except: return "Не определено"
        return "Не определено"

    async def search_google_names(self, session, phone):
        """Парсинг имен из выдачи поисковиков (Сниппеты)"""
        names = []
        try:
            # Ищем номер в кавычках для точного совпадения
            search_url = f"https://www.google.com/search?q=%22{phone}%22"
            async with session.get(search_url, headers=self.headers, timeout=7) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    # Ищем текст рядом с номером, который похож на имена
                    found = re.findall(r'([А-Я][а-я]+\s[А-Я][а-я]+)', text)
                    for n in found:
                        if len(n) > 5 and "Поиск" not in n and "Картинки" not in n:
                            names.append(n)
        except: pass
        return list(set(names))

    @loader.unrestricted
    @loader.command(ru_doc="<номер> - Полный пробив номера")
    async def shcmd(self, message):
        """Глубокий поиск данных по номеру телефона"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "❌ <b>Введите номер телефона!</b>")
            return

        phone = args.strip().replace("+", "").replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        if not phone.isdigit() or len(phone) < 10:
            await utils.answer(message, "❌ <b>Неверный формат номера.</b>")
            return

        if phone.startswith('8'): phone = '7' + phone[1:]

        status_msg = await utils.answer(message, "📡 <b>Запуск глубокого сканирования...</b>")

        async with aiohttp.ClientSession(headers=self.headers) as session:
            # 1. Регион
            await status_msg.edit("📍 <b>Определяю регион...</b>")
            region = await self.get_region(session, phone)
            
            # 2. Имена из поиска
            await status_msg.edit("🔎 <b>Парсинг поисковой выдачи...</b>")
            names = await self.search_google_names(session, phone)
            
            # 3. Формируем отчет
            res = f"🕵️‍♂️ <b>ОТЧЕТ ПО НОМЕРУ:</b> <code>+{phone}</code>\n"
            res += "━━━━━━━━━━━━━━━━━━━━\n\n"
            
            res += f"📍 <b>РЕГИОН/ОПЕРАТОР:</b>\n<code>{region}</code>\n\n"
            
            if names:
                res += "👤 <b>НАЙДЕННЫЕ ИМЕНА (Google):</b>\n"
                for i, n in enumerate(names[:5], 1):
                    res += f"  {i}. <code>{n}</code>\n"
                res += "\n"
            else:
                res += "👤 <b>ИМЯ:</b> <code>В открытом поиске не найдено</code>\n\n"

            res += "🔗 <b>МЕССЕНДЖЕРЫ (Проверь фото):</b>\n"
            res += f"  ▪️ <a href='https://wa.me/{phone}'>WhatsApp</a>\n"
            res += f"  ▪️ <a href='https://t.me/{phone}'>Telegram</a>\n\n"
            
            res += "💳 <b>БАНКОВСКИЙ ЧЕК (СБП):</b>\n"
            res += "<i>Зайди в Сбер/Т-Банк -> Платежи -> По номеру. Введи этот номер — увидишь Имя и Фамилию.</i>\n\n"
            
            res += "━━━━━━━━━━━━━━━━━━━━\n"
            res += f"🔍 <a href='https://www.google.com/search?q=%22{phone}%22'>Открыть полную выдачу Google</a>"

            await status_msg.edit(res)