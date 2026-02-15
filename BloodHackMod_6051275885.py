from hikkatl.types import Message
from .. import loader, utils
import random
import time
from datetime import datetime

@loader.tds
class BloodHackMod(loader.Module):
    """Кровавый инструмент против жыводеров"""
    strings = {
        "name": "BloodHack",
        "no_reply": "🩸 Нужна жертва (реплай)!",
        "author": "Создатель: @Python_Javs | Канал: @matrixatac"
    }

    async def client_ready(self, client, db):
        self.client = client
        await client.send_message("me", f"⚔️ <b>BloodHack активирован!</b>\n{self.strings['author']}")

    async def bloodcmd(self, message: Message):
        """Кровавая анимация"""
        blood = ["🩸", "💉", "🩹", "🩺", "🔪", "🗡", "🪓", "🧨", "💣"]
        m = await utils.answer(message, "<b>ПОДГОТОВКА КАЗНИ...</b>")
        for _ in range(15):
            blood_emoji = random.choice(blood)
            await utils.answer(
                m,
                f"<b>{blood_emoji*3} КРОВОТОК {blood_emoji*3}</b>\n"
                f"▰{'▰'*random.randint(1, 10)}{'▱'*(10-random.randint(1, 10))} {random.randint(10, 100)}%"
            )
            time.sleep(0.3)
        await utils.answer(m, "💀 <b>ЖЫВОДЕР УНИЧТОЖЕН</b> 💀")

    async def hackcmd(self, message: Message):
        """Фейковый взлом"""
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, self.strings["no_reply"])
            return

        text = f"🖥 <b>ВЗЛОМ СИСТЕМЫ</b>\nЖертва: <code>{reply.sender_id}</code>\n\n"
        m = await utils.answer(message, text + "▓▓▓▓▓▓▓▓▓▓ 0%")
        
        for i in range(1, 11):
            progress = "█"*i*2 + "▓"*(20-i*2)
            ip_part = f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"
            data_type = random.choice(["ПОЧТА", "ПАРОЛИ", "ФОТО", "ИСТОРИЯ"])
            await utils.answer(
                m,
                text + f"{progress} {i*10}%\n"
                f"├ IP: {ip_part}\n"
                f"└ ДАННЫЕ: {data_type} >> УТЕЧКА"
            )
            time.sleep(0.5)
        
        await utils.answer(
            m,
            text + "██████████ 100%\n"
            "💀 <b>ВСЕ ДАННЫЕ УНИЧТОЖЕНЫ</b> 💀\n"
            f"<code>Уничтожено: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</code>"
        )

    async def viruscmd(self, message: Message):
        """Фейковый вирус"""
        virus = ["trojan.exe", "bloodhack.dll", "matrix_v3.1.4", "killswitch.bat"]
        m = await utils.answer(message, "🦠 <b>ЗАГРУЗКА ВИРУСА...</b>")
        
        for _ in range(5):
            virus_name = random.choice(virus)
            infected = random.randint(100, 999)
            ram = random.randint(70, 99)
            await utils.answer(
                m,
                f"⚠ <b>Обнаружен {virus_name}</b>\n"
                f"├ Файлы: {infected} заражено\n"
                f"└ RAM: {ram}% загружено"
            )
            time.sleep(0.7)
        
        await utils.answer(m, "☠ <b>СИСТЕМА УНИЧТОЖЕНА</b> ☠")

    async def prankcmd(self, message: Message):
        """Жуткий пранк"""
        scary = [
            "Ты стал следующей жертвой...",
            "Мы уже идём за тобой...",
            f"Твой IP: 127.0.{random.randint(0, 255)}.{random.randint(0, 255)}",
            "Проверь свою камеру...",
            "Не оборачивайся..."
        ]
        await utils.answer(
            message,
            "👁‍🗨 <b>MATRIX NOTIFICATION</b>\n\n"
            f"{random.choice(scary)}\n\n"
            "<code>Протокол 'Кровавый рассвет' активирован</code>"
        )

    async def datacmd(self, message: Message):
        """Фейковые данные жертвы"""
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, self.strings["no_reply"])
            return

        data = [
            ("📧 Почта", f"user{random.randint(1980, 2023)}@bloodmail.com"),
            ("🔑 Пароль", "".join(random.choices("abcdef123456!@#$%", k=10))),
            ("📱 Телефон", f"+7{random.randint(900, 999)}{random.randint(1000000, 9999999)}"),
            ("🏠 Адрес", f"ул. {random.choice(['Кровавая', 'Мясницкая', 'Жертвенная'])} {random.randint(1, 99)}"),
            ("💳 Карта", f"{random.randint(4000, 4999)} **** **** {random.randint(1000, 9999)}")
        ]
        
        text = f"🔪 <b>ДАННЫЕ ЖЕРТВЫ [ID: {reply.sender_id}]</b>\n\n"
        text += "\n".join([f"├ {k}: <code>{v}</code>" for k, v in data])
        text += "\n\n🩸 <b>Эти данные будут уничтожены через 24 часа</b>"
        
        await utils.answer(message, text)

    async def paniccmd(self, message: Message):
        """Панель безумия"""
        await utils.answer(
            message,
            "☣ <b>BLOODHACK PANIC MENU</b> ☣\n\n"
            "├ .blood - Кровавая анимация\n"
            "├ .hack - Фейковый взлом\n"
            "├ .virus - Вирусная атака\n"
            "├ .prank - Жуткий пранк\n"
            "├ .data - Фейковые данные\n"
            "└ .panic - Это меню\n\n"
            f"<code>{self.strings['author']}</code>"
        )