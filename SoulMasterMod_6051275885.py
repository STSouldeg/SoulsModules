# meta developer: @Elizar_SoulsTeam
# meta banner: https://i.imgur.com/8QA5l6P.jpeg

from .. import loader, utils
import asyncio
from datetime import datetime
from telethon.tl.functions.account import UpdateProfileRequest

@loader.tds
class SoulMasterMod(loader.Module):
    """SoulMaster: Живое био (часы), Скрытое чтение и Невидимые теги."""
    strings = {
        "name": "SoulMaster",
        "clock_on": "<b>⏰ Живое био включено!</b>",
        "clock_off": "<b>⏰ Живое био выключено.</b>",
        "peek_done": "<b>👻 Сообщение 'подсмотрено' и отправлено в Избранное.</b>",
        "itag_usage": "<b>🏷 Использование: .itag @user текст</b>"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "bio_text", "Soul Set User | Time: {time}",
            "Текст био. {time} заменится на время."
        )

    async def client_ready(self, client, db):
        self.db = db
        self._client = client
        self.clock_task = None

    # --- SOUL CLOCK (Живое Био) ---
    @loader.command()
    async def bioclock(self, message):
        """Вкл/Выкл живые часы в Био"""
        status = self.db.get("SoulMaster", "clock", False)
        if not status:
            self.db.set("SoulMaster", "clock", True)
            await utils.answer(message, self.strings["clock_on"])
            self.clock_task = asyncio.create_task(self._clock_loop())
        else:
            self.db.set("SoulMaster", "clock", False)
            await utils.answer(message, self.strings["clock_off"])
            if self.clock_task:
                self.clock_task.cancel()

    async def _clock_loop(self):
        while self.db.get("SoulMaster", "clock"):
            current_time = datetime.now().strftime("%H:%M")
            new_bio = self.config["bio_text"].format(time=current_time)
            try:
                await self._client(UpdateProfileRequest(about=new_bio))
            except:
                pass
            await asyncio.sleep(60)

    # --- SOUL PEEK (Скрытое чтение) ---
    @loader.command()
    async def peek(self, message):
        """(reply) - Прочитать сообщение без уведомления (не ставить галочки)"""
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, "<b>❌ Ответь на сообщение!</b>")
            return

        text = reply.text or "<i>[Медиа без текста]</i>"
        sender = await reply.get_sender()
        name = utils.get_display_name(sender)

        log_msg = f"<b>👻 SoulPeek (Скрытое чтение):</b>\n<b>👤 От:</b> {name}\n\n{text}"
        await message.client.send_message("me", log_msg)
        await message.delete()

    # --- SOUL ITAG (Невидимый тег) ---
    @loader.command()
    async def itag(self, message):
        """<@user> <текст> - Тегнуть человека невидимо"""
        args = utils.get_args_raw(message).split(maxsplit=1)
        if len(args) < 2:
            await utils.answer(message, self.strings["itag_usage"])
            return

        user_raw = args[0]
        text = args[1]
        
        try:
            user = await message.client.get_entity(user_raw)
            # Создаем невидимый тег через ссылку на пробеле
            mention = f"<a href='tg://user?id={user.id}'>\xad</a>"
            await utils.answer(message, f"{text}{mention}")
        except:
            await utils.answer(message, "<b>❌ Пользователь не найден.</b>")