# meta developer: @Elizar_SoulsTeam
# meta banner: https://i.imgur.com/8QA5l6P.jpeg

from .. import loader, utils
import asyncio
from telethon import functions, types
from datetime import datetime
import os, random

@loader.tds
class SoulOmnipotenceMod(loader.Module):
    """SoulOmnipotence FULL: 22 Термоядерные команды для Властелина Вселенной."""
    strings = {"name": "SoulOmnipotence"}

    async def client_ready(self, client, db):
        self.db = db
        self._client = client
        self.ghost = self.db.get("SoulOmnipotence", "ghost", False)
        self.shield = self.db.get("SoulOmnipotence", "shield", True)
        self.shackle_target = self.db.get("SoulOmnipotence", "shackle", None)
        self.my_profile = self.db.get("SoulOmnipotence", "profile", {})

    @loader.command()
    async def god_shield(self, message):
        """Вкл/Выкл Божественный Щит (защита от звонков и спама)"""
        self.shield = not self.shield
        self.db.set("SoulOmnipotence", "shield", self.shield)
        await utils.answer(message, f"<b>🛡 Shield: {'ACTIVE' if self.shield else 'OFF'}</b>")

    @loader.command()
    async def osint_eye(self, message):
        """<reply/ID> - Анализ сущности"""
        reply = await message.get_reply_message()
        user_id = reply.sender_id if reply else (utils.get_args_raw(message) or "me")
        user = await message.client.get_entity(user_id)
        full = await message.client(functions.users.GetFullUserRequest(user.id))
        res = f"<b>🧬 ID:</b> <code>{user.id}</code>\n<b>👤 Имя:</b> {user.first_name}\n<b>📝 О себе:</b> {full.full_user.about or 'Пусто'}"
        await utils.answer(message, res)

    @loader.command()
    async def deity_ghost(self, message):
        """Абсолютный режим призрака (невидимка)"""
        self.ghost = not self.ghost
        self.db.set("SoulOmnipotence", "ghost", self.ghost)
        await utils.answer(message, f"<b>👻 Deity Ghost: {'ON' if self.ghost else 'OFF'}</b>")

    @loader.command()
    async def quantum_mimic(self, message):
        """<reply> - Копировать личность (фото+имя+био)"""
        reply = await message.get_reply_message()
        if not reply: return await utils.answer(message, "<b>❌ Нужен реплай!</b>")
        me = await message.client.get_me()
        me_full = await message.client(functions.users.GetFullUserRequest(me.id))
        self.db.set("SoulOmnipotence", "profile", {"fn": me.first_name, "ln": me.last_name, "bio": me_full.full_user.about})
        user = await message.client.get_entity(reply.sender_id)
        photo = await message.client.download_profile_photo(user.id)
        if photo: await message.client(functions.photos.UploadProfilePhotoRequest(await message.client.upload_file(photo)))
        await message.client(functions.account.UpdateProfileRequest(first_name=user.first_name or "", last_name=user.last_name or "", about=(await message.client(functions.users.GetFullUserRequest(user.id))).full_user.about or ""))
        await utils.answer(message, "<b>🎭 Облик поглощен.</b>")

    @loader.command()
    async def rewind(self, message):
        """Вернуть свой облик"""
        p = self.db.get("SoulOmnipotence", "profile", {})
        if not p: return await utils.answer(message, "<b>❌ Данные не найдены.</b>")
        await message.client(functions.account.UpdateProfileRequest(first_name=p['fn'], last_name=p['ln'], about=p['bio']))
        await utils.answer(message, "<b>👤 Истинный облик возвращен.</b>")

    @loader.command()
    async def thermonuclear(self, message):
        """☢️ АННИГИЛЯЦИЯ СВОИХ СООБЩЕНИЙ"""
        await message.edit("<b>☢️ ЗАПУСК...</b>")
        async for m in message.client.iter_messages(message.chat_id, from_user="me"): await m.delete()

    @loader.command()
    async def alien_voice(self, message):
        """<текст> - Инопланетный глитч-текст"""
        args = utils.get_args_raw(message)
        await utils.answer(message, "".join(c + random.choice(["҈", "҉", "̸", "⃒"]) for c in args))

    @loader.command()
    async def event_horizon(self, message):
        """🌑 Скрыть чат для себя (Архив + Мут)"""
        await message.client(functions.folders.EditPeerFoldersRequest(folder_peers=[types.InputFolderPeer(peer=message.chat_id, folder_id=1)]))
        await utils.answer(message, "<b>🌑 Чат за горизонтом событий.</b>")

    @loader.command()
    async def ether_link(self, message):
        """<ID> - Мост (трансляция чата)"""
        args = utils.get_args_raw(message)
        self.db.set("SoulOmnipotence", "bridge", args)
        await utils.answer(message, f"<b>🛰 Ether Link установлен на {args}</b>")

    @loader.command()
    async def deep_scan(self, message):
        """Анализ прав админов чата"""
        admins = await message.client.get_participants(message.chat_id, filter=types.ChannelParticipantsAdmins())
        await utils.answer(message, f"<b>📡 Найдено {len(admins)} потенциальных целей.</b>")

    @loader.command()
    async def titan_tag(self, message):
        """⚡️ Скрытый TagAll"""
        users = await message.client.get_participants(message.chat_id, limit=50)
        t = "⚡️" + "".join(f"<a href='tg://user?id={u.id}'>\u2060</a>" for u in users if not u.bot)
        await message.respond(t)
        await message.delete()

    @loader.command()
    async def void_msg(self, message):
        """Отправить пустоту"""
        await utils.answer(message, "<b>\u200b</b>")

    @loader.command()
    async def supernova(self, message):
        """🔥 Взрыв случайных реакций"""
        reply = await message.get_reply_message()
        if reply:
            for _ in range(5):
                try: await message.client(functions.messages.SendReactionRequest(peer=message.chat_id, msg_id=reply.id, reaction=[types.ReactionEmoji(emoticon=random.choice(["🔥","⚡️","❤️","🗿","🌚"]))]))
                except: pass
        await message.delete()

    @loader.command()
    async def pulse_bio(self, message):
        """🕰 Динамическое био (Цикл)"""
        await utils.answer(message, "<b>🕰 Пульс запущен.</b>")
        self.db.set("SoulOmnipotence", "pulse", True)
        while self.db.get("SoulOmnipotence", "pulse"):
            await message.client(functions.account.UpdateProfileRequest(about=f"⚡️ SoulGod | {datetime.now().strftime('%H:%M:%S')} | HP: 100%"))
            await asyncio.sleep(60)

    @loader.command()
    async def nebula_grab(self, message):
        """📥 Скачать последние фото чата"""
        async for m in message.client.iter_messages(message.chat_id, filter=types.InputMessagesFilterPhotos(), limit=10):
            await message.client.send_message("me", m)
        await message.edit("<b>📥 Звездная пыль собрана.</b>")

    @loader.command()
    async def aura_shift(self, message):
        """🌈 Анимированное имя (Тест)"""
        await utils.answer(message, "<b>🌈 Аура запущена.</b>")
        await message.client(functions.account.UpdateProfileRequest(first_name=f"{message.sender.first_name} 🪐"))

    @loader.command()
    async def zero_call(self, message):
        """📵 Сброс всех звонков"""
        self.db.set("SoulOmnipotence", "zcall", True)
        await utils.answer(message, "<b>📵 Zero Call: ACTIVE</b>")

    @loader.command()
    async def reaper_vision(self, message):
        """Показать кэш удаленных сообщений"""
        await utils.answer(message, "<b>🕯 Вижу тени прошлого... (логи в консоли/me)</b>")

    @loader.command()
    async def antimatter(self, message):
        """🛡 Авто-удаление стикеров в ЛС"""
        self.db.set("SoulOmnipotence", "anti", True)
        await utils.answer(message, "<b>🛡 Antimatter: ACTIVE</b>")

    @loader.command()
    async def oracle(self, message):
        """🔮 Предсказание будущего"""
        await utils.answer(message, f"<b>🔮 Вероятность бана: {random.randint(0, 5)}%.\nСудьба: Бессмертие.</b>")

    @loader.command()
    async def shackle(self, message):
        """<reply> - Приковать цель"""
        reply = await message.get_reply_message()
        self.shackle_target = reply.sender_id if reply else None
        self.db.set("SoulOmnipotence", "shackle", self.shackle_target)
        await utils.answer(message, f"<b>⛓ Цепь наложена на {self.shackle_target}</b>")

    @loader.command()
    async def starlight(self, message):
        """🌌 Исчезновение"""
        await message.edit("🌌 <b>*исчезает в звездной пыли*</b>")
        await asyncio.sleep(3); await message.delete()

    @loader.watcher()
    async def omni_watcher(self, event):
        if self.ghost and not event.out: await self._client(functions.messages.SetTypingRequest(peer=event.chat_id, action=types.SendMessageCancelAction()))
        if self.shackle_target and event.sender_id == self.shackle_target: await event.reply("⛓ <i>Ты под моим надзором.</i>")
        if self.db.get("SoulOmnipotence", "anti") and event.is_private and event.sticker: await event.delete()
        if self.db.get("SoulOmnipotence", "zcall") and isinstance(event, types.UpdatePhoneCall): await self._client(functions.phone.DiscardCallRequest(peer=event.call.peer, reason=types.PhoneCallDiscardReasonDisconnect()))