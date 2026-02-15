# meta developer: @Elizar_SoulsTeam
# requires: aiohttp

from telethon import functions, types
import aiohttp
import re
from .. import loader, utils

@loader.tds
class SoulsIntelMod(loader.Module):
    """🕵️‍♂️ SoulsIntel v7.0: Пробив через внутреннюю базу Telegram и реестры"""
    
    strings = {"name": "SoulsIntel 🕵️‍♂️"}

    async def get_region_info(self, phone):
        """Получение региона через API реестров"""
        async with aiohttp.ClientSession() as session:
            try:
                # Используем API для определения оператора и региона
                async with session.get(f"https://rosreestr.subnets.ru/api.php?p={phone}", timeout=5) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        region = data.get('region', 'Не найден')
                        operator = data.get('operator', 'Не найден')
                        return f"{region} ({operator})"
            except:
                return "Не удалось определить"

    @loader.unrestricted
    @loader.command(ru_doc="<номер> - Прямой поиск по базе Telegram")
    async def shcmd(self, message):
        """Поиск владельца номера в базе Telegram и реестрах"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "❌ <b>Введите номер телефона!</b>")
            return

        phone = args.strip().replace("+", "").replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        if not phone.isdigit() or len(phone) < 10:
            await utils.answer(message, "❌ <b>Некорректный формат номера.</b>")
            return

        status_msg = await utils.answer(message, "📡 <b>Поиск в базе данных Telegram...</b>")

        # Пытаемся импортировать контакт, чтобы вытянуть инфу
        contact = types.InputPhoneContact(client_id=0, phone=phone, first_name="Search", last_name="Souls")
        
        try:
            result = await message.client(functions.contacts.ImportContactsRequest([contact]))
            
            region_info = await self.get_region_info(phone)
            
            if result.users:
                user = result.users[0]
                full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
                username = f"@{user.username}" if user.username else "Скрыт"
                user_id = user.id
                bio_obj = await message.client(functions.users.GetFullUserRequest(user.id))
                bio = bio_obj.full_user.about or "Не указано"
                
                res = f"🕵️‍♂️ <b>РЕЗУЛЬТАТЫ ПОИСКА:</b>\n"
                res += "━━━━━━━━━━━━━━━━━━━━\n\n"
                res += f"👤 <b>ИМЯ В TG:</b> <code>{full_name}</code>\n"
                res += f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
                res += f"🔗 <b>USERNAME:</b> {username}\n"
                res += f"📝 <b>О СЕБЕ:</b> <code>{bio}</code>\n\n"
                res += f"📍 <b>РЕГИОН:</b> <code>{region_info}</code>\n"
                res += "━━━━━━━━━━━━━━━━━━━━\n"
                res += "💳 <b>ПРОВЕРКА В БАНКАХ (СБП):</b>\n"
                res += "<i>Для получения ФИО попробуйте 'перевод по номеру' в приложении вашего банка.</i>\n\n"
                res += f"🌐 <b>ПОИСК В СЕТИ:</b> <a href='https://www.google.com/search?q=%22{phone}%22'>Найти упоминания</a>"
                
                # Удаляем контакт после проверки, чтобы не засорять книгу
                await message.client(functions.contacts.DeleteContactsRequest(id=[user.id]))
            else:
                res = f"🕵️‍♂️ <b>ОТЧЕТ ПО НОМЕРУ:</b> <code>+{phone}</code>\n"
                res += "━━━━━━━━━━━━━━━━━━━━\n\n"
                res += "❌ <b>В базе Telegram номер не найден.</b>\n"
                res += f"📍 <b>РЕГИОН:</b> <code>{region_info}</code>\n\n"
                res += "💡 <i>Скорее всего, номер не привязан к аккаунту или скрыт настройками приватности.</i>\n"
                res += f"🌐 <b>ПОИСК В СЕТИ:</b> <a href='https://www.google.com/search?q=%22{phone}%22'>Найти в Google</a>"

            await status_msg.edit(res)

        except Exception as e:
            await status_msg.edit(f"❌ <b>Ошибка при запросе к API:</b> <code>{str(e)}</code>")