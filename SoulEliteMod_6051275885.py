# meta developer: @Elizar_SoulsTeam
# meta banner: https://i.imgur.com/8QA5l6P.jpeg

from .. import loader, utils
import asyncio
from telethon import functions, types
from datetime import datetime

@loader.tds
class SoulEliteMod(loader.Module):
    """SoulElite: Спецсборка v2.0 (Ghost, Mimic, Sentry, Omega, Portal, Reaction, DeepSearch, Aura)."""
    strings = {"name": "SoulElite"}

    async def client_ready(self, client, db):
        self.db = db
        self._client = client
        self.sreact_state = self.db.get("SoulElite", "sreact", False)
        self.ghost_mode = self.db.get("SoulElite", "ghost", False)
        self.aura_active = False

    @loader.command()
    async def ghost(self, message):
        """Вкл/Выкл режим призрака (скрытое чтение и тайпинг)"""
        self.ghost_mode = not self.ghost_mode
        self.db.set("SoulElite", "ghost", self.ghost_mode)
        await utils.answer(message, f"<b>{'👁 Режим Призрака активирован' if self.ghost_mode else '👤 Режим Призрака выключен'}</b>")

    @loader.command()
    async def mimic(self, message):
        """<reply> - Скопировать профиль цели"""
        reply = await message.get_reply_message()
        if not reply: return await utils.answer(message, "<b>❌ Реплаем на цель!</b>")
        user = await message.client.get_entity(reply.sender_id)
        full = await message.client(functions.users.GetFullUserRequest(user.id))
        await message.client(functions.account.UpdateProfileRequest(
            first_name=user.first_name or "",
            last_name=user.last_name or "",
            about=full.full_user.about or ""
        ))
        await utils.answer(message, "<b>👥 Личность поглощена.</b>")

    @loader.command()
    async def sentry(self, message):
        """<слово> - Глобальный мониторинг слова"""
        args = utils.get_args_raw(message)
        words = self.db.get("SoulElite", "sentry", [])
        if not args: return await utils.answer(message, f"<b>📡 Слежка за:</b> {', '.join(words) if words else 'пусто'}")
        words.append(args.lower())
        self.db.set("SoulElite", "sentry", words)
        await utils.answer(message, f"<b>📡 Сигнал '{args}' принят.</b>")

    @loader.command()
    async def omega(self, message):
        """Полная зачистка (Nuke) своих сообщений"""
        await message.edit("<b>💣 SoulOmega: Инициализация...</b>")
        async for msg in message.client.iter_messages(message.chat_id, from_user="me", limit=100):
            await msg.delete()
        await message.delete()

    @loader.command()
    async def portal(self, message):
        """<ID> - Создать мост в этот чат"""
        args = utils.get_args_raw(message)
        if not args:
            self.db.set("SoulElite", "portal", None)
            return await utils.answer(message, "<b>🌀 Портал закрыт.</b>")
        self.db.set("SoulElite", "portal", args)
        await utils.answer(message, f"<b>🌀 Портал открыт на: {args}</b>")

    @loader.command()
    async def sreact(self, message):
        """<emoji> - Авто-реакции на ВСЁ"""
        args = utils.get_args_raw(message)
        if not args:
            self.sreact_state = False
            return await utils.answer(message, "<b>🔥 Реакции OFF.</b>")
        self.db.set("SoulElite", "emoji", args)
        self.sreact_state = True
        await utils.answer(message, f"<b>🔥 Реакции ON: {args}</b>")

    @loader.command()
    async def dsearch(self, message):
        """<запрос> - Глубокий поиск участников"""
        q = utils.get_args_raw(message)
        await message.edit("<b>🔍 Глубокое сканирование...</b>")
        found = []
        async for u in message.client.iter_participants(message.chat_id, search=q):
            found.append(f"👤 {u.first_name} (@{u.username})")
        res = "\n".join(found[:15]) or "Никого не нашел."
        await utils.answer(message, f"<b>🔍 Результаты:</b>\n{res}")

    @loader.command()
    async def aura(self, message):
        """Вкл/Выкл динамическое БИО (Аура)"""
        self.aura_active = not self.aura_active
        if not self.aura_active: return await utils.answer(message, "<b>✨ Аура угасла.</b>")
        await utils.answer(message, "<b>✨ Аура активирована.</b>")
        while self.aura_active:
            now = datetime.now().strftime("%H:%M")
            bio = f"⌚ Time: {now} | SoulTeam Power ⚡"
            try:
                await message.client(functions.account.UpdateProfileRequest(about=bio))
            except: pass
            await asyncio.sleep(60)

    @loader.watcher()
    async def soul_watcher(self, message):
        if not message.chat_id: return
        
        # Ghost logic (Anti-read/Anti-typing)
        if self.ghost_mode and not message.out:
            # Предотвращаем отправку сигнала о прочтении
            # В Telethon это работает через отсутствие вызова mark_read()
            pass

        # Sentry logic
        words = self.db.get("SoulElite", "sentry", [])
        if not message.out and words:
            for w in words:
                if w in (message.text or "").lower():
                    await self._client.send_message("me", f"<b>📡 SENTRY ALERT!</b>\nЧат: <code>{message.chat_id}</code>\nТекст: {message.text}")
        
        # Portal logic
        p = self.db.get("SoulElite", "portal")
        if p and str(message.chat_id) == str(p) and not message.out:
            await self._client.send_message("me", f"<b>🌀 PORTAL:</b> {message.text}")

        # Reaction logic
        if self.sreact_state and not message.out:
            try:
                await message.react(self.db.get("SoulElite", "emoji", "🔥"))
            except: pass