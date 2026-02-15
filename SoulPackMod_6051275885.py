# meta developer: @Elizar_SoulsTeam
# meta banner: https://i.imgur.com/8QA5l6P.jpeg

from .. import loader, utils
import asyncio

@loader.tds
class SoulPackMod(loader.Module):
    """Эксклюзивный пак для Elizar_SoulsTeam (v2).
    Включает: Чистку, Фейк-действия, Валентинки и Автоответчик.
    Исправлена ошибка с зависимостями."""
    
    strings = {
        "name": "SoulPack",
        "cleaning": "<b>🗑 Начинаю зачистку мертвых душ...</b>",
        "cleaned": "<b>✅ Удалено мертвых аккаунтов: {}</b>",
        "no_rights": "<b>❌ У меня нет прав администратора (Ban Users).</b>",
        "fake_on": "<b>🎭 Фейк-статус [{}] активирован.</b>\nОстановится через 5 минут или при отправке сообщения.",
        "val_1": "<b>💖 Лови валентинку!</b>\n\n<i>Ты самое дорогое, что есть в этом чате...</i> 🌹",
        "val_2": "<b>💌 Тебе письмо!</b>\n\n( ˘ZN˘) ♡ (˘▽˘ )\n<i>Спасибо, что ты есть!</i>",
        "auto_added": "<b>🤖 Автоответчик включен для этого чата!</b>",
        "auto_removed": "<b>🔕 Автоответчик выключен для этого чата.</b>",
        "auto_reply_set": "<b>📝 Текст автоответчика установлен:</b>\n{}",
        "no_reply_text": "<b>❌ Сначала установи текст командой .setreply <текст></b>"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "auto_reply_text", "Я сейчас занят, отвечу позже! (Автоответчик)",
            "Текст для автоответчика"
        )
        # Инициализация хранилища чатов будет в client_ready

    async def client_ready(self, client, db):
        self.db = db
        self._client = client
        # Создаем список чатов, если его нет
        if self.db.get("SoulPack", "chats") is None:
            self.db.set("SoulPack", "chats", [])

    # --- ЧИСТКА (Без лишних импортов) ---
    @loader.command()
    async def deadclean(self, message):
        """Удалить удаленные аккаунты из чата"""
        if not message.chat:
            return
            
        chat = await message.get_chat()
        # Простая проверка прав
        if not (chat.admin_rights or chat.creator):
             await utils.answer(message, self.strings["no_rights"])
             return

        await utils.answer(message, self.strings["cleaning"])
        
        removed_count = 0
        # Получаем участников (работает даже на старых версиях)
        participants = await message.client.get_participants(message.chat)
        
        for user in participants:
            if user.deleted:
                try:
                    await message.client.kick_participant(message.chat_id, user.id)
                    removed_count += 1
                except:
                    pass
                    
        await utils.answer(message, self.strings["cleaned"].format(removed_count))

    # --- ФЕЙК ДЕЙСТВИЯ ---
    @loader.command()
    async def ftype(self, message):
        """<сек> - Имитация 'печатает...'"""
        args = utils.get_args(message)
        sec = int(args[0]) if args and args[0].isdigit() else 300
        await message.delete()
        async with message.client.action(message.chat_id, "typing"):
            await asyncio.sleep(sec)

    @loader.command()
    async def fvoice(self, message):
        """<сек> - Имитация 'записывает гс...'"""
        args = utils.get_args(message)
        sec = int(args[0]) if args and args[0].isdigit() else 300
        await message.delete()
        async with message.client.action(message.chat_id, "record-audio"):
            await asyncio.sleep(sec)
            
    @loader.command()
    async def fgame(self, message):
        """<сек> - Имитация 'играет в игру...'"""
        args = utils.get_args(message)
        sec = int(args[0]) if args and args[0].isdigit() else 300
        await message.delete()
        async with message.client.action(message.chat_id, "game"):
            await asyncio.sleep(sec)

    # --- ВАЛЕНТИНКИ ---
    @loader.command()
    async def val(self, message):
        """Отправить милую валентинку"""
        await utils.answer(message, self.strings["val_1"])
        hearts = ["❤️", "🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "🤍", "💖"]
        for i in hearts:
            await asyncio.sleep(0.5)
            try:
                await message.edit(f"<b>💖 Лови валентинку!</b>\n\n{i} <i>Ты супер!</i> {i}")
            except:
                break

    @loader.command()
    async def love(self, message):
        """Отправить романтичную валентинку"""
        await utils.answer(message, self.strings["val_2"])

    # --- АВТООТВЕТЧИК ---
    @loader.command()
    async def setreply(self, message):
        """<текст> - Установить текст автоответчика"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "<b>❌ Введите текст!</b>")
            return
        self.config["auto_reply_text"] = args
        await utils.answer(message, self.strings["auto_reply_set"].format(args))

    @loader.command()
    async def soulauto(self, message):
        """Вкл/Выкл автоответчик в ТЕКУЩЕМ чате"""
        chats = self.db.get("SoulPack", "chats", [])
        chat_id = message.chat_id
        
        if chat_id in chats:
            chats.remove(chat_id)
            self.db.set("SoulPack", "chats", chats)
            await utils.answer(message, self.strings["auto_removed"])
        else:
            chats.append(chat_id)
            self.db.set("SoulPack", "chats", chats)
            await utils.answer(message, self.strings["auto_added"])

    @loader.watcher(only_messages=True)
    async def watcher(self, message):
        if not hasattr(self, "db"): return
        
        chats = self.db.get("SoulPack", "chats", [])
        if message.chat_id not in chats:
            return
            
        # Не отвечать самому себе и ботам
        me = await message.client.get_me()
        if message.sender_id == me.id or message.sender.bot:
            return
            
        # Не отвечать на команды
        if message.text and message.text.startswith("."):
            return

        # Ответ (с задержкой)
        await asyncio.sleep(2)
        await message.reply(self.config["auto_reply_text"])