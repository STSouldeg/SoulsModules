# meta developer: @Elizar_SoulsTeam
import time
import asyncio
from .. import loader, utils

@loader.tds
class SoulsGuardMod(loader.Module):
    """🛡 SoulsGuard: Твой щит и контроль приватности"""
    
    strings = {"name": "SoulsGuard 🛡"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            "AFK_TEXT", "🚫 Я сейчас не в сети. Оставьте сообщение.", "Текст автоответа при AFK"
        )
        self.afk = False
        self.reason = ""
        self.start_time = 0

    @loader.command(ru_doc="[причина] - Включить режим AFK")
    async def afkcmd(self, message):
        """Уйти в AFK (автоответчик)"""
        args = utils.get_args_raw(message)
        self.afk = True
        self.reason = args if args else "Не указана"
        self.start_time = time.time()
        
        await utils.answer(message, f"🛡 <b>Режим AFK включен.</b>\n📝 <b>Причина:</b> <code>{self.reason}</code>")

    @loader.command(ru_doc="[число] - Удалить сообщения")
    async def purgecmd(self, message):
        """Быстрое удаление сообщений"""
        args = utils.get_args_raw(message)
        if not args or not args.isdigit():
            count = 10
        else:
            count = int(args)

        await message.delete()
        async for msg in message.client.iter_messages(message.chat_id, limit=count):
            try:
                await msg.delete()
            except:
                pass

    @loader.command(ru_doc="<сек> <текст> - Самоудаляющееся сообщение")
    async def selfcmd(self, message):
        """Отправить сообщение с таймером удаления"""
        args = utils.get_args_raw(message).split(" ", 1)
        if len(args) < 2 or not args[0].isdigit():
            await utils.answer(message, "❌ <b>Формат: .self [секунды] [текст]</b>")
            return

        sec = int(args[0])
        text = args[1]
        
        await message.edit(f"⏳ <i>Это сообщение удалится через {sec} сек.</i>\n\n{text}")
        await asyncio.sleep(sec)
        await message.delete()

    @loader.watcher("only_messages", "only_private", "only_mentions")
    async def afk_watcher(self, message):
        """Следит за упоминаниями и отключает AFK при твоей активности"""
        # Если ты сам что-то написал - выключаем AFK
        if message.sender_id == (await message.client.get_me()).id:
            if self.afk:
                self.afk = False
                end_time = time.time()
                duration = utils.format_duration(int(end_time - self.start_time))
                await message.respond(f"🛡 <b>Я вернулся!</b>\n⌛️ <b>Отсутствовал:</b> <code>{duration}</code>")
            return

        # Если ты в AFK и тебя тегнули или написали в ЛС
        if self.afk:
            if message.is_private or message.mentioned:
                end_time = time.time()
                duration = utils.format_duration(int(end_time - self.start_time))
                reply = f"🛡 <b>{self.config['AFK_TEXT']}</b>\n"
                reply += f"📝 <b>Причина:</b> <code>{self.reason}</code>\n"
                reply += f"⌛️ <b>Меня нет уже:</b> <code>{duration}</code>"
                await message.reply(reply)