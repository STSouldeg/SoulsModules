# -*- coding: utf-8 -*-
from .. import loader, utils
from telethon.tl.types import Message
from datetime import datetime
import time

@loader.tds
class MegaChatTools(loader.Module):
    """Универсальный модуль для чатов с управлением"""
    strings = {
        "name": "MegaChatTools",
        "on": "✅ Модуль включен в этом чате",
        "off": "❌ Модуль отключен в этом чате",
        "welcome": "👋 Добро пожаловать, {user} в {chat}!",
        "warn": "⚠ {user}, получил предупреждение ({count}/3)",
        "kicked": "🚷 {user} был исключен за нарушения",
        "rep_plus": "👍 +1 к репутации {user} (теперь: {rep})",
        "rep_minus": "👎 -1 к репутации {user} (теперь: {rep})",
        "not_allowed": "🚫 Этот чат не настроен для работы модуля"
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.reputation = self.db.get("MegaChatTools", "reputation", {})
        self.user_warns = self.db.get("MegaChatTools", "warns", {})
        self.active_chats = self.db.get("MegaChatTools", "active_chats", [])
        self.module_state = self.db.get("MegaChatTools", "module_state", True)

    async def togglecmd(self, message):
        """Включить/выключить модуль в этом чате"""
        chat_id = message.chat_id
        if chat_id in self.active_chats:
            self.active_chats.remove(chat_id)
            await message.edit(self.strings["off"])
        else:
            self.active_chats.append(chat_id)
            await message.edit(self.strings["on"])
        self.db.set("MegaChatTools", "active_chats", self.active_chats)

    async def globaltogglecmd(self, message):
        """Глобально включить/выключить модуль"""
        self.module_state = not self.module_state
        status = "включен" if self.module_state else "выключен"
        await message.edit(f"🔄 Модуль глобально {status}")
        self.db.set("MegaChatTools", "module_state", self.module_state)

    def is_active(self, chat_id):
        """Проверка активности модуля в чате"""
        return self.module_state and chat_id in self.active_chats

    async def watcher(self, message):
        """Автомодерация"""
        if not isinstance(message, Message) or not self.is_active(message.chat_id):
            return
            
        # Автоудаление ссылок
        if "http://" in message.text or "https://" in message.text:
            if not await self.is_admin(message.chat_id, message.sender_id):
                await message.delete()
                await self.warn_user(message)
                
        # Защита от флуда
        if self.is_flood(message):
            await message.delete()
            await self.warn_user(message)

    async def welcomecmd(self, message):
        """Включить приветствия (только для админов)"""
        if not self.is_active(message.chat_id):
            return await message.edit(self.strings["not_allowed"])
        
        if not await self.is_admin(message.chat_id, message.sender_id):
            return await message.edit("🚫 Только админы могут использовать эту команду")
            
        chat = await message.get_chat()
        await message.edit(f"Приветствия включены для {chat.title}")

    async def rep_pluscmd(self, message):
        """+1 к репутации"""
        if not self.is_active(message.chat_id):
            return await message.edit(self.strings["not_allowed"])
            
        user = await self.get_user(message)
        uid = str(user.id)
        self.reputation[uid] = self.reputation.get(uid, 0) + 1
        await message.edit(self.strings["rep_plus"].format(
            user=user.first_name,
            rep=self.reputation[uid]
        ))
        self.db.set("MegaChatTools", "reputation", self.reputation)

    async def quizcmd(self, message):
        """Викторина"""
        if not self.is_active(message.chat_id):
            return await message.edit(self.strings["not_allowed"])
            
        question = "Столица России?"
        answers = ["Москва", "Питер", "Казань"]
        correct = 0
        
        await message.edit(
            f"❓ {question}\n\n" +
            "\n".join(f"{i}. {a}" for i, a in enumerate(answers, 1))
        )

    async def get_user(self, message):
        reply = await message.get_reply_message()
        return reply.sender if reply else message.sender

    async def is_admin(self, chat_id, user_id):
        try:
            participants = await self.client.get_participants(chat_id)
            for p in participants:
                if p.id == user_id and (p.admin_rights or p.creator):
                    return True
            return False
        except:
            return False

    def is_flood(self, message):
        """Проверка на флуд"""
        return False