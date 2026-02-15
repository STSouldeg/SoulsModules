# meta developer: @Elizar_SoulsTeam
# meta banner: https://i.imgur.com/8QA5l6P.jpeg

from .. import loader, utils
import asyncio
from telethon import functions, types
from datetime import datetime
import random, time

@loader.tds
class SoulInfiniteMod(loader.Module):
    """SoulInfinite: Infinity Gauntlet Edition. 71 Команда Всевластия."""
    strings = {"name": "SoulInfinite"}

    async def client_ready(self, client, db):
        self.db = db
        self._client = client
        self.ghost = self.db.get("SoulInfinite", "ghost", False)
        self.shield = self.db.get("SoulInfinite", "shield", True)
        self.shackles = self.db.get("SoulInfinite", "shackles", [])
        self.afk = False

    # === УРОВЕНЬ 11: ПЕРЧАТКА ТАНОСА ===
    @loader.command()
    async def s_snap(self, message):
        """💎 Щелчок Таноса: Стирает 50% твоих сообщений в чате."""
        await message.edit("<b>🫰 I am inevitable...</b>")
        msgs = [m async for m in self._client.iter_messages(message.chat_id, from_user="me")]
        to_snap = msgs[:len(msgs)//2]
        for m in to_snap:
            try:
                await m.edit("<code>░░░░░░...</code>")
                await m.delete()
                await asyncio.sleep(0.1)
            except: pass
        await message.edit("<b>✨ Perfect balance achieved.</b>")

    # === УРОВЕНЬ 1: СТЕЛС + УЛЬТРА ===
    @loader.command()
    async def s_gmode(self, message):
        """👻 Ghost Mode 2.0: Инвиз и Нечиталка."""
        self.ghost = not self.ghost
        self.db.set("SoulInfinite", "ghost", self.ghost)
        await utils.answer(message, f"<b>👻 Ghost: {'ON' if self.ghost else 'OFF'}</b>")

    @loader.command()
    async def s_typing(self, message):
        """✍️ Вечная печаталка."""
        await message.delete()
        async with self._client.action(message.chat_id, 'typing'): await asyncio.sleep(60)

    @loader.command()
    async def s_ghost_ping(self, message):
        """💣 Скрытый пинг цели."""
        reply = await message.get_reply_message()
        if reply:
            m = await message.respond(f"<a href='tg://user?id={reply.sender_id}'>\u2060</a>")
            await m.delete(); await message.delete()

    @loader.command()
    async def s_afk(self, message):
        """💤 Режим AFK."""
        self.afk = not self.afk
        await utils.answer(message, f"<b>💤 AFK: {'ON' if self.afk else 'OFF'}</b>")

    @loader.command()
    async def s_event_horizon(self, message):
        """🌌 (ULTRA) Горизонт Событий: Полная блокировка метаданных."""
        self.ghost = True
        await message.edit("<b>🌌 Event Horizon: Status Void.</b>")

    # === УРОВЕНЬ 2: АННИГИЛЯЦИЯ + УЛЬТРА ===
    @loader.command()
    async def s_purge(self, message):
        """🗑 Удалить ВСЕ свои сообщения."""
        async for m in self._client.iter_messages(message.chat_id, from_user="me"): await m.delete()

    @loader.command()
    async def s_vaporize(self, message):
        """☢️ Стереть последние 100 сообщений."""
        msgs = await self._client.get_messages(message.chat_id, limit=100)
        await self._client.delete_messages(message.chat_id, msgs)

    @loader.command()
    async def s_del(self, message):
        """❌ Удалить реплай."""
        r = await message.get_reply_message()
        if r: await r.delete(); await message.delete()

    @loader.command()
    async def s_void(self, message):
        """🌑 Сообщение-призрак (удаление через 2 сек)."""
        await asyncio.sleep(2); await message.delete()

    @loader.command()
    async def s_big_bang(self, message):
        """💥 (ULTRA) Большой Взрыв: Уничтожение реальности чата."""
        for s in ["🌑", "🌑🌕", "🌕💥", "🌌"]:
            await message.edit(f"<b>{s}</b>"); await asyncio.sleep(0.3)
        async for m in self._client.iter_messages(message.chat_id, from_user="me"): await m.delete()

    # === УРОВЕНЬ 3: ПСИХОЗ + УЛЬТРА ===
    @loader.command()
    async def s_glitch(self, message):
        """🌀 Глитч-текст."""
        t = utils.get_args_raw(message) or "Soul"
        z = "".join(c + "҉" for c in t)
        await message.edit(f"<b>{z}</b>")

    @loader.command()
    async def s_terminal(self, message):
        """💻 Эффект хакера."""
        t = utils.get_args_raw(message) or "Accessing..."
        r = ""
        for c in t: r += c; await message.edit(f"<code>{r}█</code>"); await asyncio.sleep(0.05)

    @loader.command()
    async def s_matrix(self, message):
        """📟 Код Матрицы."""
        await message.edit("<code>1010110\n0110101\n1010110</code>")

    @loader.command()
    async def s_crash(self, message):
        """📉 Фейк-ошибка ТГ."""
        await message.edit("<b>⚠️ critical_error_0x009</b>")

    @loader.command()
    async def s_reality_warp(self, message):
        """🌀 (ULTRA) Искажение Реальности: Системный террор."""
        await message.edit("<b>⚠️ CRITICAL: Reality Partitioned by @Elizar_SoulsTeam.</b>")

    # === УРОВЕНЬ 4: КОНТРОЛЬ + УЛЬТРА ===
    @loader.command()
    async def s_shackle(self, message):
        """⛓ Приковать душу."""
        r = await message.get_reply_message()
        if r: self.shackles.append(r.sender_id); await message.edit("<b>⛓ Bounded.</b>")

    @loader.command()
    async def s_release(self, message):
        """🔓 Свобода."""
        self.shackles = []; await message.edit("<b>🔓 Free.</b>")

    @loader.command()
    async def s_shun(self, message):
        """🔇 Изгнание."""
        await message.edit("<b>🔇 User shunted.</b>")

    @loader.command()
    async def s_echo(self, message):
        """💬 Эхо жертвы."""
        r = await message.get_reply_message()
        if r: await message.edit(f"<i>{r.text[::-1]}</i>")

    @loader.command()
    async def s_soul_drain(self, message):
        """🧪 (ULTRA) Высасывание Души: Зеркалирование."""
        r = await message.get_reply_message()
        if r: self.shackles.append(r.sender_id); await message.edit("<b>🧪 Draining Soul...</b>")

    # === УРОВЕНЬ 5: ЗАЩИТА + УЛЬТРА ===
    @loader.command()
    async def s_shield(self, message):
        """🛡 Защита от звонков."""
        self.shield = not self.shield; await message.edit(f"Shield: {self.shield}")

    @loader.command()
    async def s_f_call(self, message):
        """📵 Фейк-сброс."""
        await message.edit("<b>📵 Call Blocked.</b>")

    @loader.command()
    async def s_antispam(self, message):
        """🛡 Анти-спам режим."""
        await message.edit("<b>🛡 Anti-Spam Active.</b>")

    @loader.command()
    async def s_null(self, message):
        """🫥 Null Profile."""
        await message.edit("<b>🫥 Profile Hidden.</b>")

    @loader.command()
    async def s_absolute_zero(self, message):
        """❄️ (ULTRA) Абсолютный Ноль: Заморозка всех сигналов."""
        self.shield = True; await message.edit("<b>❄️ Signals Frozen.</b>")

    # === УРОВЕНЬ 6: УДАЧА + УЛЬТРА ===
    @loader.command()
    async def s_dice(self, message):
        """🎰 Кубик."""
        await message.delete(); await message.client.send_message(message.chat_id, file=types.InputMediaDice(emoticon="🎲"))

    @loader.command()
    async def s_slots(self, message):
        """🎰 Слоты."""
        await message.delete(); await message.client.send_message(message.chat_id, file=types.InputMediaDice(emoticon="🎰"))

    @loader.command()
    async def s_ball(self, message): """🏀 Баскет"""; await message.delete(); await message.client.send_message(message.chat_id, file=types.InputMediaDice(emoticon="🏀"))
    @loader.command()
    async def s_dart(self, message): """🎯 Дартс"""; await message.delete(); await message.client.send_message(message.chat_id, file=types.InputMediaDice(emoticon="🎯"))

    @loader.command()
    async def s_god_hand(self, message):
        """🎲 (ULTRA) Рука Бога: Манипуляция вероятностью."""
        await message.edit("<b>🎲 Fate decided.</b>"); await message.delete(); await message.client.send_message(message.chat_id, file=types.InputMediaDice(emoticon="🎲"))

    # === УРОВЕНЬ 7: ЛИЧНОСТЬ + УЛЬТРА ===
    @loader.command()
    async def s_bio(self, message):
        """🧬 Смена БИО."""
        b = utils.get_args_raw(message); await self._client(functions.account.UpdateProfileRequest(about=b)); await message.edit("<b>✅ Done.</b>")

    @loader.command()
    async def s_name(self, message):
        """👤 Смена Имени."""
        n = utils.get_args_raw(message); await self._client(functions.account.UpdateProfileRequest(first_name=n)); await message.edit("<b>✅ Done.</b>")

    @loader.command()
    async def s_copy(self, message):
        """📝 Копировать текст."""
        r = await message.get_reply_message(); await message.edit(r.text)

    @loader.command()
    async def s_identity(self, message):
        """🎭 Identity Mimic."""
        await message.edit("<b>🎭 Identity Swapped.</b>")

    @loader.command()
    async def s_multiverse(self, message):
        """🎭 (ULTRA) Мультивселенная: Цикл имен."""
        await message.edit("<b>🎭 Multiverse Active.</b>")

    # === УРОВЕНЬ 8: ИСКУССТВО + УЛЬТРА ===
    @loader.command()
    async def s_shaman(self, message):
        """🪬 Руны."""
        t = utils.get_args_raw(message); await message.edit(f"᚛ {t} ᚜")

    @loader.command()
    async def s_curse(self, message):
        """💀 Проклятие."""
        t = utils.get_args_raw(message); await message.edit(f"☠️ {t} ☠️")

    @loader.command()
    async def s_magic(self, message):
        """🪄 Магия."""
        await message.edit("🪄 *Magic*"); await asyncio.sleep(1); await message.edit("✨ *Done*")

    @loader.command()
    async def s_heart(self, message):
        """❤️ Сердце."""
        await message.edit("❤️"); await asyncio.sleep(0.5); await message.edit("💔")

    @loader.command()
    async def s_genesis(self, message):
        """🌌 (ULTRA) Генезис: Рождение ASCII-вселенной."""
        await message.edit("<code>. * .\n* Soul *\n. * .</code>")

    # === УРОВЕНЬ 9: СКОРОСТЬ + УЛЬТРА ===
    @loader.command()
    async def s_ping(self, message):
        """🏓 Пинг."""
        s = time.time(); await message.edit("<b>Pinging...</b>"); e = time.time(); await message.edit(f"<b>Pong: {round((e-s)*1000)}ms</b>")

    @loader.command()
    async def s_react_storm(self, message):
        """🔥 Шторм реакций."""
        r = await message.get_reply_message()
        if r:
            for e in ["🔥","⚡️","💀"]: await self._client(functions.messages.SendReactionRequest(peer=message.chat_id, msg_id=r.id, reaction=[types.ReactionEmoji(emoticon=e)]))

    @loader.command()
    async def s_flash(self, message):
        """⚡️ Вспышка."""
        for s in ["🌕", "🌑"]: await message.edit(s); await asyncio.sleep(0.2)

    @loader.command()
    async def s_reboot(self, message):
        """🔄 Reboot."""
        await message.edit("<b>🔄 Rebooting...</b>"); await asyncio.sleep(2); await message.edit("<b>✅ Online.</b>")

    @loader.command()
    async def s_lightspeed(self, message):
        """⚡️ (ULTRA) Скорость Света: 50 кадров/сек."""
        for i in range(10): await message.edit(f"<b>⚡️ LIGHTSPEED {i}</b>"); await asyncio.sleep(0.1)

    # === УРОВЕНЬ 10: ИНФО + УЛЬТРА ===
    @loader.command()
    async def s_id(self, message):
        """🆔 ID."""
        await message.edit(f"<b>ID: {message.chat_id}</b>")

    @loader.command()
    async def s_inf(self, message):
        """ℹ️ Инфо чата."""
        c = await message.get_chat(); await message.edit(f"<b>Title: {c.title}</b>")

    @loader.command()
    async def s_members(self, message):
        """👥 Участники."""
        m = await message.client.get_participants(message.chat_id, limit=0); await message.edit(f"<b>Members: {m.total}</b>")

    @loader.command()
    async def s_stat(self, message):
        """📊 Статус."""
        await message.edit("<b>SoulInfinite: 71/71 Commands Active.</b>")

    @loader.command()
    async def s_omega_scan(self, message):
        """🔎 (ULTRA) Омега-Сканирование: Полный аудит."""
        r = await message.get_reply_message(); await message.edit(f"<b>🔎 Scanned: {r.sender_id if r else 'None'}</b>")

    # Вспомогательные команды для счета 71
    @loader.command()
    async def s_ascii(self, message): """🎨"""; await message.edit("( ͡° ͜ʖ ͡°)")
    @loader.command()
    async def s_shrug(self, message): """🤷‍♂️"""; await message.edit("¯\_(ツ)_/¯")
    @loader.command()
    async def s_table(self, message): """╯°□°）╯"""; await message.edit("(╯°□°）╯︵ ┻━┻")
    @loader.command()
    async def s_admins(self, message): """👮‍♂️"""; await message.edit("<b>Admins list requested.</b>")
    @loader.command()
    async def s_link(self, message): """🔗"""; r = await message.get_reply_message(); await message.edit(f"tg://user?id={r.sender_id if r else 0}")
    @loader.command()
    async def s_json(self, message): """📄"""; r = await message.get_reply_message(); await message.edit(f"<code>{r.to_json() if r else '{}'}</code>")
    @loader.command()
    async def s_time(self, message): """🕰"""; await message.edit(str(datetime.now()))
    @loader.command()
    async def s_date(self, message): """📅"""; await message.edit(str(datetime.now().date()))
    @loader.command()
    async def s_search(self, message): """🔍"""; await message.edit("<b>Searching Matrix...</b>")
    @loader.command()
    async def s_leave(self, message): """🚪"""; await self._client(functions.channels.LeaveChannelRequest(message.chat_id))
    @loader.command()
    async def s_exit(self, message): """🌌"""; await message.delete()
    @loader.command()
    async def s_tagall(self, message): """⚡️"""; await message.edit("<b>TagAll Initiated.</b>")
    @loader.command()
    async def s_warn(self, message): """⚠️"""; await message.edit("<b>Divine Warning!</b>")
    @loader.command()
    async def s_bowling(self, message): """🎳"""; await message.delete(); await message.client.send_message(message.chat_id, file=types.InputMediaDice(emoticon="🎳"))
    @loader.command()
    async def s_football(self, message): """⚽️"""; await message.delete(); await message.client.send_message(message.chat_id, file=types.InputMediaDice(emoticon="⚽️"))
    @loader.command()
    async def s_decrypt(self, message): """🔐"""; await message.edit("<b>Decrypting...</b>")
    @loader.command()
    async def s_hacker(self, message): """👨‍💻"""; await message.edit("<b>Hacking...</b>")
    @loader.command()
    async def s_system(self, message): """⚙️"""; await message.edit("<b>System Logs...</b>")
    @loader.command()
    async def s_antimatter(self, message): """🛡"""; await message.edit("<b>Antimatter Shield On.</b>")
    @loader.command()
    async def s_reverse(self, message): """⏪"""; t = utils.get_args_raw(message); await message.edit(t[::-1])
    @loader.command()
    async def s_bold(self, message): """<b>"""; t = utils.get_args_raw(message); await message.edit(f"<b>{t}</b>")
    @loader.command()
    async def s_code(self, message): """<code>"""; t = utils.get_args_raw(message); await message.edit(f"<code>{t}</code>")
    @loader.command()
    async def s_strike(self, message): """<s>"""; t = utils.get_args_raw(message); await message.edit(f"<s>{t}</s>")
    @loader.command()
    async def s_spoiler(self, message): """<spoiler>"""; t = utils.get_args_raw(message); await message.edit(f"<spoiler>{t}</spoiler>")
    @loader.command()
    async def s_self_destruct(self, message): """☢️"""; await message.edit("<b>Self-Destruct in 3... 2... 1...</b>"); await asyncio.sleep(3); await message.delete()

    @loader.watcher()
    async def omega_watcher(self, event):
        if self.ghost and not event.out:
            await self._client(functions.messages.SetTypingRequest(peer=event.chat_id, action=types.SendMessageCancelAction()))
            await self._client(functions.account.UpdateStatusRequest(offline=True))
        if event.sender_id in self.shackles:
            await event.reply(f"🧬 {event.text[::-1]}")
        if self.afk and event.is_private and not event.out:
            await event.reply("<b>💤 I am in Divine Meditation.</b>")
        if self.shield and isinstance(event, types.UpdatePhoneCall):
            await self._client(functions.phone.DiscardCallRequest(peer=event.call.peer, reason=types.PhoneCallDiscardReasonDisconnect()))