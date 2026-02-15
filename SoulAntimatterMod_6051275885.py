# meta developer: @Elizar_SoulsTeam
# meta banner: https://i.imgur.com/8QA5l6P.jpeg

from .. import loader, utils
import asyncio
from telethon import functions, types
from datetime import datetime
import random, os

@loader.tds
class SoulAntimatterMod(loader.Module):
    """SoulAntimatter: Divine Overlord Edition. 30 ядерных команд."""
    strings = {"name": "SoulAntimatter"}

    async def client_ready(self, client, db):
        self.db = db
        self._client = client
        self.ghost = self.db.get("SoulAntimatter", "ghost", False)
        self.shield = self.db.get("SoulAntimatter", "shield", True)
        self.shackles = self.db.get("SoulAntimatter", "shackles", [])
        self.targets = self.db.get("SoulAntimatter", "targets", [])

    @loader.command()
    async def gmode(self, message):
        """Вкл/Выкл True Ghost 2.0 (Инвиз + Нечиталка)"""
        self.ghost = not self.ghost
        self.db.set("SoulAntimatter", "ghost", self.ghost)
        await utils.answer(message, f"<b>👻 Ghost 2.0: {'ACTIVE' if self.ghost else 'OFF'}</b>")

    @loader.command()
    async def blackhole(self, message):
        """🕳 Аннигиляция реальности (100 сообщений)"""
        await message.edit("<b>🕳 Горизонт событий расширяется...</b>")
        async for m in message.client.iter_messages(message.chat_id, limit=100, from_user="me"):
            await m.delete()

    @loader.command()
    async def terminal(self, message):
        """☣️ Эффект хакера"""
        text = utils.get_args_raw(message) or "Initializing SoulAntimatter Breach..."
        res = ""
        for char in text:
            res += char
            await message.edit(f"<code>{res}█</code>")
            await asyncio.sleep(0.05)

    @loader.command()
    async def singularity(self, message):
        """🌑 Сообщение из сингулярности"""
        args = utils.get_args_raw(message)
        await utils.answer(message, f"<b>{' '.join([c + '҉' for c in args])}</b>")

    @loader.command()
    async def judgment(self, message):
        """⚖️ Визуальный бан цели (Фейк)"""
        reply = await message.get_reply_message()
        name = reply.sender.first_name if reply else "User"
        await message.edit(f"<b>🛑 SYSTEM: User {name} has been banned for: Violation of Divine Protocol.</b>")

    @loader.command()
    async def brainfuck(self, message):
        """👹 Демонический шифр"""
        args = utils.get_args_raw(message)
        bf = "".join(random.choice(["⛧", "☠", "⚔", "☣", "☢", "⸸"]) + c for c in args)
        await utils.answer(message, f"<code>{bf}</code>")

    @loader.command()
    async def loading_fake(self, message):
        """📊 Анимация взлома"""
        for i in range(0, 101, 10):
            await message.edit(f"<b>📡 Data Breach: {i}% [ {'#'*(i//10)}{'-'*(10-i//10)} ]</b>")
            await asyncio.sleep(0.2)
        await message.edit("<b>✅ SYSTEM COMPROMISED.</b>")

    @loader.command()
    async def soul_shackle(self, message):
        """⛓ Приковать душу (реплай)"""
        reply = await message.get_reply_message()
        if reply:
            self.shackles.append(reply.sender_id)
            self.db.set("SoulAntimatter", "shackles", self.shackles)
            await utils.answer(message, "<b>⛓ Душа в оковах антиматерии.</b>")

    @loader.command()
    async def release(self, message):
        """🔓 Свобода для всех"""
        self.shackles = []
        self.db.set("SoulAntimatter", "shackles", [])
        await utils.answer(message, "<b>🔓 Все оковы пали.</b>")

    @loader.command()
    async def flash(self, message):
        """⚡️ Вспышка"""
        t = utils.get_args_raw(message)
        for s in ["🌕", "🌗", "🌑", "⚡️", t]:
            await message.edit(f"<b>{s}</b>")
            await asyncio.sleep(0.3)

    @loader.command()
    async def rigged_dice(self, message):
        """🎰 Подкрученные кости"""
        await message.delete()
        await message.client.send_message(message.chat_id, file=types.InputMediaDice(emoticon="🎲"))

    @loader.command()
    async def system_crash(self, message):
        """📉 Фейк краш"""
        await message.edit("<b>⚠️ Fatal Error: Telegram UI Process stopped. (Exception: Soul_Overload)</b>")

    @loader.command()
    async def chaos(self, message):
        """🌀 Выброс хаоса"""
        for _ in range(5):
            await message.client.send_message(message.chat_id, "🌀")
        await message.delete()

    @loader.command()
    async def echo_soul(self, message):
        """💬 Искаженное эхо (реплай)"""
        reply = await message.get_reply_message()
        if reply: await message.respond(f"👤 <b>{reply.sender.first_name} сказал:</b> <i>{reply.text[::-1]}</i> (Soul Echo)")

    @loader.watcher()
    async def god_watcher(self, event):
        if self.ghost and not event.out:
            await self._client(functions.messages.SetTypingRequest(peer=event.chat_id, action=types.SendMessageCancelAction()))
            await self._client(functions.account.UpdateStatusRequest(offline=True))
        if event.sender_id in self.shackles:
            phrases = ["Твое существование бесполезно.", "Твои слова — шум в пустоте.", "⛓ Смирись.", "Свет затухает..."]
            await event.reply(f"<i>{random.choice(phrases)}</i>")
        if self.shield and isinstance(event, types.UpdatePhoneCall):
            await self._client(functions.phone.DiscardCallRequest(peer=event.call.peer, reason=types.PhoneCallDiscardReasonDisconnect()))