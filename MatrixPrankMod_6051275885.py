from hikkatl.types import Message
from .. import loader, utils
import random

@loader.tds
class MatrixPrankMod(loader.Module):
    """Модуль для страшных пранков в стиле MATRIX"""
    strings = {
        "name": "MatrixPrank",
        "no_reply": "🔪 Нужен реплай на жертву!",
        "prank_url": "https://httpbin.org/status/200",  # Изменено на httpbin
        "fake_info": (
            "🩸 <b>MATRIX EXE SYSTEM v3.1.4</b> 🩸\n\n"
            "💀 <b>ЦЕЛЬ ЗАХВАЧЕНА:</b>\n"
            "├ <b>ID:</b> <code>{user_id}</code>\n"
            "├ <b>IP:</b> <code>{ip}</code>\n"
            "├ <b>LOCATION:</b> {city}, {country}\n"
            "├ <b>PROVIDER:</b> {provider}\n"
            "├ <b>VPN:</b> {vpn}\n"
            "└ <b>DEVICE:</b> {device}\n\n"
            "⚠️ <b>WARNING: SYSTEM FAILURE DETECTED</b>"
        ),
        "prank_text": (
            "👁️ <b>MATRIX EXE NOTIFICATION</b> 👁️\n\n"
            "⚠️ <b>CRITICAL SYSTEM ALERT</b>\n"
            "Обнаружен доступ к запрещенным данным:\n"
            "{url}\n\n"
            "<code>ИНИЦИИРОВАН ПРОТОКОЛ 'КРОВАВЫЙ МЕСЯЦ'</code>\n"
            "▰▰▰▰▰▰▰▰▰▰ 100%\n\n"
            "<b>||ДАННЫЕ УНИЧТОЖЕНЫ||</b>"
        )
    }

    async def client_ready(self, client, db):
        self.client = client

    async def matrixcmd(self, message: Message):
        """Показать фейковую информацию в стиле MATRIX"""
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, self.strings("no_reply"))
            return

        user_id = reply.sender_id
        ip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        providers = ["SKYNET", "UMBRELLA CORP", "BLACK MESA", "WEYLAND-YUTANI"]
        cities = ["CITY 17", "RAVENHOLM", "NOVIGRAD", "DUNWALL"]
        countries = ["ZONE 51", "OUTER HAVEN", "THE WASTELAND"]
        devices = ["TERMINAL #"+str(random.randint(1000,9999)), "CYBERDINE SYSTEMS T-800", "UMBRELLA BIO-COMPUTER"]

        fake_data = {
            "user_id": user_id,
            "ip": ip,
            "provider": random.choice(providers),
            "city": random.choice(cities),
            "country": random.choice(countries),
            "vpn": random.choice(["DETECTED", "TERMINATED", "CORRUPTED"]),
            "device": random.choice(devices)
        }

        await utils.answer(
            message,
            self.strings("fake_info").format(**fake_data)
        )

    async def prankcmd(self, message: Message):
        """Отправить страшный пранк"""
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, self.strings("no_reply"))
            return

        await utils.answer(
            message,
            self.strings("prank_text").format(url=self.strings("prank_url"))
        )

    async def setprankurlcmd(self, message: Message):
        """Установить свою пранк-ссылку"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "🩸 Нужно указать URL КРОВАВОГО МЕСЯЦА!")
            return

        self.strings["prank_url"] = args
        await utils.answer(message, f"🖥️ <b>MATRIX EXE</b>: URL установлен: <code>{args}</code>")