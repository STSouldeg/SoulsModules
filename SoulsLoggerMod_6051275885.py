# meta developer: @Elizar_SoulsTeam

import logging
from .. import loader, utils
from telethon.tl.types import Message

logger = logging.getLogger(__name__)

@loader.tds
class SoulsLoggerMod(loader.Module):
    """🕵️‍♂️ SoulsLogger: Логирование удаленных и измененных сообщений"""
    strings = {"name": "SoulsLogger"}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.cache = self.db.get("SoulsLogger", "cache", [])
        self.log_chat = self.db.get("SoulsLogger", "log_chat", "me")
        self.status = self.db.get("SoulsLogger", "status", True)

    @loader.command(ru_doc="Включить/выключить логгер")
    async def logtogglecmd(self, message):
        """Переключить статус логгера"""
        self.status = not self.status
        self.db.set("SoulsLogger", "status", self.status)
        state = "ВКЛЮЧЕН" if self.status else "ВЫКЛЮЧЕН"
        await utils.answer(message, f"🕵️‍♂️ <b>Логгер теперь {state}</b>")

    @loader.command(ru_doc="Установить текущий чат как чат для логов")
    async def logsetcmd(self, message):
        """Установить чат логов"""
        self.log_chat = message.chat_id
        self.db.set("SoulsLogger", "log_chat", self.log_chat)
        await utils.answer(message, "📂 <b>Этот чат установлен как хранилище логов!</b>")

    @loader.watcher(only_messages=True, out=False)
    async def watcher(self, message):
        if not self.status or not message.text:
            return

        # Кэшируем сообщение (сохраняем ID, текст и данные автора)
        msg_data = {
            "id": message.id,
            "chat_id": message.chat_id,
            "text": message.text,
            "sender": message.sender_id,
            "user": (await message.get_sender()).first_name if message.sender else "Unknown"
        }
        
        self.cache.append(msg_data)
        if len(self.cache) > 500: # Лимит кэша для Термукса
            self.cache.pop(0)
        self.db.set("SoulsLogger", "cache", self.cache)

    @loader.watcher(only_messages=True, out=False, edit=True)
    async def edit_watcher(self, message):
        if not self.status or not message.text:
            return

        # Ищем старую версию в кэше
        old_msg = next((m for m in self.cache if m["id"] == message.id and m["chat_id"] == message.chat_id), None)
        
        if old_msg and old_msg["text"] != message.text:
            log_text = (
                f"📝 <b>Сообщение изменено!</b>\n"
                f"👤 <b>От:</b> <code>{old_msg['user']}</code>\n"
                f"📍 <b>Чат:</b> <code>{message.chat_id}</code>\n\n"
                f"❌ <b>Было:</b>\n{old_msg['text']}\n\n"
                f"✅ <b>Стало:</b>\n{message.text}"
            )
            await self.client.send_message(self.log_chat, log_text)
            
            # Обновляем кэш
            old_msg["text"] = message.text
            self.db.set("SoulsLogger", "cache", self.cache)

    # Примечание: Telegram API не присылает текст при удалении, 
    # поэтому логгер удалений в юзерботах работает только через перехват событий удаления ID.
    # В этой версии фокус на самом важном — Редактировании.