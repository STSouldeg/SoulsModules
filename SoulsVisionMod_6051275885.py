# meta developer: @Elizar_SoulsTeam
# requires: aiohttp

import aiohttp
from .. import loader, utils

@loader.tds
class SoulsVisionMod(loader.Module):
    """🕵️‍♂️ SoulsVision v9.0: Профессиональный OSINT-инструмент"""
    
    strings = {"name": "SoulsVision 🕵️‍♂️"}

    async def get_info(self, phone):
        """Регион и оператор через стабильное API"""
        async with aiohttp.ClientSession() as session:
            try:
                # Используем надежное API для определения региона
                async with session.get(f"https://rosreestr.subnets.ru/api.php?p={phone}", timeout=5) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get('region', 'Неизвестен'), data.get('operator', 'Неизвестен')
            except:
                return "Не определен", "Не определен"
        return "Не определен", "Не определен"

    @loader.unrestricted
    @loader.command(ru_doc="<номер> - Запуск OSINT-панели")
    async def shcmd(self, message):
        """Запуск панели поиска по номеру"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "❌ <b>Введите номер телефона!</b>")
            return

        phone = args.strip().replace("+", "").replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        if not phone.isdigit() or len(phone) < 10:
            await utils.answer(message, "❌ <b>Неверный формат номера.</b>")
            return

        if phone.startswith('8'): phone = '7' + phone[1:]

        status_msg = await utils.answer(message, "⚙️ <b>Подготовка OSINT-панели...</b>")

        region, operator = await self.get_info(phone)

        res = f"🕵️‍♂️ <b>OSINT-ОТЧЕТ:</b> <code>+{phone}</code>\n"
        res += "━━━━━━━━━━━━━━━━━━━━\n\n"
        
        res += f"📍 <b>ЛОКАЦИЯ:</b> <code>{region}</code>\n"
        res += f"📱 <b>ОПЕРАТОР:</b> <code>{operator}</code>\n\n"
        
        res += "📂 <b>БЫСТРЫЙ ПОИСК (Нажми для результата):</b>\n"
        res += f"  🔹 <a href='https://mirror.bullshit.agency/search_by_phone/{phone}'>Проверить ТЕГИ (GetContact)</a>\n"
        res += f"  🔹 <a href='https://zvonili.com/phone/{phone}'>Посмотреть отзывы и ФИО</a>\n"
        res += f"  🔹 <a href='https://www.google.com/search?q=%22{phone}%22'>Поиск упоминаний в Google</a>\n\n"
        
        res += "💬 <b>МЕССЕНДЖЕРЫ:</b>\n"
        res += f"  ▪️ <a href='https://t.me/{phone}'>Telegram</a> | <a href='https://wa.me/{phone}'>WhatsApp</a> | <a href='viber://add?number={phone}'>Viber</a>\n\n"
        
        res += "💳 <b>КАК УЗНАТЬ ФИО ЗА 10 СЕКУНД:</b>\n"
        res += "1. Зайди в приложение любого банка (Сбер, Т-Банк).\n"
        res += "2. Выбери 'Перевод по номеру телефона'.\n"
        res += f"3. Введи <code>{phone}</code>.\n"
        res += "4. Ты увидишь <b>Имя, Отчество и первую букву Фамилии</b> владельца абсолютно бесплатно.\n"
        
        res += "━━━━━━━━━━━━━━━━━━━━\n"
        res += "⚠️ <i>Бесплатные скрипты не могут выводить ФИО текстом из-за защиты сайтов. Используй ссылки выше.</i>"

        await status_msg.edit(res)