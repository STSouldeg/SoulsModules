# meta developer: @Elizar_SoulsTeam
# requires: aiohttp

import aiohttp
import asyncio
from .. import loader, utils

@loader.tds
class SoulsSherlockMod(loader.Module):
    """🕵️‍♂️ SoulsSherlock v10.0: Логика Sherlock + Поиск по номеру"""
    
    strings = {"name": "SoulsSherlock 🕵️‍♂️"}

    def __init__(self):
        self.sites = {
            "Instagram": "https://www.instagram.com/{}",
            "GitHub": "https://github.com/{}",
            "VK": "https://vk.com/{}",
            "Steam": "https://steamcommunity.com/id/{}",
            "Pinterest": "https://www.pinterest.com/{}",
            "TikTok": "https://www.tiktok.com/@{}",
            "Twitter": "https://twitter.com/{}",
            "Twitch": "https://www.twitch.content/{}",
            "Telegram": "https://t.me/{}"
        }

    async def check_username(self, session, site, url_mask, username):
        url = url_mask.format(username)
        try:
            async with session.get(url, timeout=5) as resp:
                if resp.status == 200:
                    return f"✅ <b>{site}:</b> {url}"
                return None
        except:
            return None

    async def get_phone_info(self, phone):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"https://rosreestr.subnets.ru/api.php?p={phone}", timeout=5) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return f"📍 <b>Регион:</b> <code>{data.get('region', 'Не найден')}</code>\n📱 <b>Оператор:</b> <code>{data.get('operator', 'Не найден')}</code>"
            except:
                return "📍 <b>Регион:</b> <code>Не определен</code>"
        return "📍 <b>Регион:</b> <code>Не определен</code>"

    @loader.unrestricted
    @loader.command(ru_doc="<ник или номер> - Запуск Sherlock-поиска")
    async def shcmd(self, message):
        """Поиск по нику (Sherlock) или номеру телефона"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "❌ <b>Введите ник или номер!</b>")
            return

        query = args.strip()
        
        # Проверяем, номер это или ник
        is_phone = query.replace("+", "").replace(" ", "").isdigit()

        if is_phone:
            phone = query.replace("+", "").replace(" ", "").replace("-", "")
            if phone.startswith('8'): phone = '7' + phone[1:]
            
            status = await utils.answer(message, f"🔎 <b>Пробив номера</b> <code>+{phone}</code><b>...</b>")
            info = await self.get_phone_info(phone)
            
            res = f"🕵️‍♂️ <b>ОТЧЕТ ПО НОМЕРУ:</b> <code>+{phone}</code>\n"
            res += "━━━━━━━━━━━━━━━━━━━━\n\n"
            res += f"{info}\n\n"
            res += "🔗 <b>СВЯЗЬ:</b>\n"
            res += f"  ▪️ <a href='https://t.me/{phone}'>Telegram</a> | <a href='https://wa.me/{phone}'>WhatsApp</a>\n\n"
            res += "📂 <b>БАЗЫ ТЕГОВ (Открыть вручную):</b>\n"
            res += f"  🔹 <a href='https://mirror.bullshit.agency/search_by_phone/{phone}'>GetContact Mirror</a>\n"
            res += f"  🔹 <a href='https://zvonili.com/phone/{phone}'>База Zvonili</a>\n\n"
            res += "💳 <b>СБП (ФИО):</b>\n"
            res += "<i>Проверь номер в приложении банка (Сбер/Т-Банк) через 'Перевод по номеру' — это даст ФИО бесплатно.</i>"
            
            await status.edit(res)
        
        else:
            # Логика Sherlock (поиск по нику)
            status = await utils.answer(message, f"🕵️‍♂️ <b>Sherlock запускает поиск по нику:</b> <code>{query}</code>...")
            
            found_sites = []
            async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
                tasks = [self.check_username(session, site, url, query) for site, url in self.sites.items()]
                results = await asyncio.gather(*tasks)
                found_sites = [r for r in results if r]

            res = f"🔍 <b>РЕЗУЛЬТАТЫ SHERLOCK ДЛЯ:</b> <code>{query}</code>\n"
            res += "━━━━━━━━━━━━━━━━━━━━\n\n"
            
            if found_sites:
                res += "\n".join(found_sites)
            else:
                res += "❌ <b>Аккаунтов с таким ником не найдено.</b>"
            
            res += "\n\n━━━━━━━━━━━━━━━━━━━━\n"
            res += f"🌐 <a href='https://www.google.com/search?q={query}'>Поиск в Google</a>"
            
            await status.edit(res)