from .. import loader, utils
import asyncio
import random
from telethon.tl.types import Message

@loader.tds
class TerminatorXMod(loader.Module):
    """Терминатор Х - система контроля"""
    
    strings = {
        "name": "TerminatorX",
        "welcome": (
            "╔══════════════════════╗\n"
            "║   ТЕРМИНАТОР Х v9.0  ║\n"
            "║    СИСТЕМА ЗАПУСКА   ║\n"
            "╚══════════════════════╝\n"
        ),
        "login": "⌛ Подключаюсь к серверу...",
        "auth": "🔐 Требуется аутентификация",
        "success": "✅ Доступ разрешен",
        "failed": "⛔ Неверные учетные данные",
        "menu": (
            "╔══════════════════════╗\n"
            "║   АДМИН ПАНЕЛЬ  Х9   ║\n"
            "╠══════════════════════╣\n"
            "║ 1. Статус системы    ║\n"
            "║ 2. Запустить процесс ║\n"
            "║ 3. Экстренный стоп   ║\n"
            "║ 4. Сканирование сети ║\n"
            "║ 5. Скрытый режим     ║\n"
            "╚══════════════════════╝\n"
            "\nВведите код команды:"
        ),
        "process_start": "⚡ Инициализация процесса...",
        "scan": "🔍 Сканирование сети:",
        "hidden": "👁️ Активирован скрытый режим"
    }

    def __init__(self):
        self.authenticated = False
        self.admin_pass = "Admin"  # Измените на свой пароль
        self.admin_login = "Admin"    # Измените на свой логин

    async def client_ready(self, client, db):
        self._client = client
        self._db = db

    async def txcmd(self, message: Message):
        """Активация системы TerminatorX"""
        args = utils.get_args_raw(message)
        
        if not self.authenticated:
            # Анимация запуска
            msg = await utils.answer(message, self.strings["welcome"])
            await asyncio.sleep(1)
            
            await msg.edit(self.strings["welcome"] + "\n" + self.strings["login"])
            await asyncio.sleep(2)
            
            await msg.edit(self.strings["welcome"] + "\n" + self.strings["auth"])
            await asyncio.sleep(1)
            
            if not args:
                await msg.edit(
                    self.strings["welcome"] + "\n" +
                    "🔐 Логин: _\n"
                    "🔑 Пароль: _\n\n"
                    "Используйте: .tx логин пароль"
                )
                return
                
            try:
                login, password = args.split(maxsplit=1)
                if login == self.admin_login and password == self.admin_pass:
                    self.authenticated = True
                    await msg.edit(
                        self.strings["welcome"] + "\n" +
                        f"🔐 Логин: {login}\n"
                        f"🔑 Пароль: {'*'*len(password)}\n\n" +
                        self.strings["success"]
                    )
                    await asyncio.sleep(1)
                    await self.show_menu(msg)
                else:
                    await msg.edit(
                        self.strings["welcome"] + "\n" +
                        f"🔐 Логин: {login}\n"
                        f"🔑 Пароль: {'*'*len(password)}\n\n" +
                        self.strings["failed"]
                    )
            except:
                await msg.edit("⚠️ Ошибка формата: .tx логин пароль")
        else:
            await self.handle_command(message, args)

    async def show_menu(self, msg):
        """Показать меню админ-панели"""
        await msg.edit(self.strings["welcome"] + "\n" + self.strings["menu"])

    async def handle_command(self, message, cmd):
        """Обработка команд меню"""
        msg = await utils.answer(message, "⌛ Обработка запроса...")
        
        if cmd == "1":
            status = (
                "╔══════════════════════╗\n"
                "║   СТАТУС СИСТЕМЫ     ║\n"
                "╠══════════════════════╣\n"
                f"║ Загрузка CPU: {random.randint(1, 100)}%      ║\n"
                f"║ Память: {random.randint(300, 900)}MB/{random.randint(1,2)}GB   ║\n"
                "║ Статус: АКТИВЕН      ║\n"
                "╚══════════════════════╝"
            )
            await msg.edit(status)
            
        elif cmd == "2":
            await msg.edit(self.strings["process_start"])
            await asyncio.sleep(1)
            for i in range(1, 6):
                await msg.edit(f"{self.strings['process_start']}\n{'█'*i*4} {i*20}%")
                await asyncio.sleep(0.5)
            await msg.edit("✅ Процесс успешно запущен")
            
        elif cmd == "3":
            await msg.edit("🛑 Активация экстренного останова...")
            for i in range(5, 0, -1):
                await msg.edit(f"🛑 Останов через {i}...")
                await asyncio.sleep(1)
            await msg.edit("✅ Система остановлена")
            self.authenticated = False
            
        elif cmd == "4":
            scan_result = (
                f"{self.strings['scan']}\n"
                "├─ 192.168.1.1: ✓ ONLINE\n"
                "├─ 192.168.1.2: ✗ OFFLINE\n"
                "├─ 192.168.1.3: ✓ ONLINE\n"
                "└─ 192.168.1.4: ✓ ONLINE\n\n"
                "Найдено 3 активных хоста"
            )
            await msg.edit(scan_result)
            
        elif cmd == "5":
            await msg.edit(self.strings["hidden"])
            await asyncio.sleep(1)
            await msg.edit("👁️‍🗨️ Все следы удалены")
            
        else:
            await self.show_menu(msg)