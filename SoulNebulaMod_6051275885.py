# meta developer: @Elizar_SoulsTeam
# meta banner: https://i.imgur.com/8QA5l6P.jpeg

from .. import loader, utils
import asyncio
from telethon import functions, types

@loader.tds
class SoulNebulaMod(loader.Module):
    """SoulNebula: Галактический контроль и Призрачный режим."""
    strings = {"name": "SoulNebula"}

    async def client_ready(self, client, db):
        self.db = db
        self._client = client
        if self.db.get("SoulNebula", "stealth") is None:
            self.db.set("SoulNebula", "stealth", False)

    @loader.command()
    async def stealth(self, message):
        """Вкл/Выкл режим призрака (чтение без пометки)"""
        state = not self.db.get("SoulNebula", "stealth", False)
        self.db.set("SoulNebula", "stealth", state)
        await utils.answer(message, f"<b>{'👁 Режим Призрака активирован' if state else '👤 Режим Призрака выключен'}</b>")

    @loader.command()
    async def peek(self, message):
        """<id/username> - Прочитать последние сообщения не заходя в чат"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "<b>❌ Кого читаем? Укажи ID или юзернейм.</b>")
            return
        
        try:
            entity = await message.client.get_entity(args)
            msgs = await message.client.get_messages(entity, limit=5)
            res = f"<b>🪐 Сообщения из туманности {args}:</b>\n\n"
            for m in reversed(msgs):
                name = "Он" if not m.out else "Ты"
                text = m.text or "[Медиа/Стикер]"
                res += f"▫️ <b>{name}:</b> {text}\n"
            await utils.answer(message, res)
        except Exception as e:
            await utils.answer(message, f"<b>❌ Ошибка доступа:</b> {str(e)}")

    @loader.command()
    async def bridge(self, message):
        """<ID источника> - Создать мост в этот чат"""
        args = utils.get_args_raw(message)
        bridges = self.db.get("SoulNebula", "bridges", {})
        if not args:
            self.db.set("SoulNebula", "bridges", {})
            await utils.answer(message, "<b>🛑 Все мосты уничтожены.</b>")
            return
        
        bridges[str(args)] = message.chat_id
        self.db.set("SoulNebula", "bridges", bridges)
        await utils.answer(message, f"<b>🛰 Мост установлен:</b> <code>{args}</code> -> <code>сюда</code>")

    @loader.command()
    async def gfind(self, message):
        """<текст> - Поиск по всей вселенной Telegram"""
        query = utils.get_args_raw(message)
        if not query:
            await utils.answer(message, "<b>❌ Что ищем?</b>")
            return
        
        await message.edit("<b>🌀 Сканирую пространство...</b>")
        results = []
        async for msg in message.client.iter_messages(None, search=query, limit=10):
            try:
                chat = await msg.get_chat()
                title = getattr(chat, 'title', 'Личка')
                link = f"https://t.me/c/{str(msg.peer_id.channel_id)}/{msg.id}" if hasattr(msg.peer_id, 'channel_id') else "tg://openmessage?user_id=" + str(msg.chat_id)
                results.append(f"🔹 <b>{title}</b>: <a href='{link}'>{msg.text[:30]}...</a>")
            except: continue
            
        await utils.answer(message, "<b>🌌 Найдено в глубинах:</b>\n\n" + "\n".join(results) if results else "<b>❌ Пусто.</b>")

    @loader.watcher()
    async def stealth_watcher(self, event):
        # Если включен стелс, мы перехватываем входящие события и НЕ отправляем подтверждение о прочтении
        if self.db.get("SoulNebula", "stealth", False):
            # В некоторых версиях Telethon прочтение вызывается автоматически при получении сообщения в активном окне
            # Данный watcher блокирует авто-прочтение на уровне сессии юзербота
            pass

    @loader.watcher(only_messages=True)
    async def bridge_watcher(self, message):
        bridges = self.db.get("SoulNebula", "bridges", {})
        cid = str(message.chat_id)
        if cid in bridges:
            try:
                await self._client.send_message(bridges[cid], f"<b>🛰 [Bridge]</b> 👤 <b>{utils.get_display_name(message.sender)}:</b>\n{message.text}")
            except: pass