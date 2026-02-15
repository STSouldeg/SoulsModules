# meta developer: @Elizar_SoulsTeam
# meta banner: https://i.imgur.com/8QA5l6P.jpeg

from .. import loader, utils
import asyncio

@loader.tds
class SoulFakeMod(loader.Module):
    """SoulFake: Имитация активности в чате."""
    strings = {
        "name": "SoulFake",
        "started": "<b>🎭 Статус [{}] запущен.</b>\nЧтобы остановить, напиши <code>.sfs</code>",
        "stopped": "<b>🛑 Все фейк-статусы остановлены.</b>",
        "unknown": "<b>❌ Неизвестный тип.</b>\nДоступные: <code>typing, voice, video, photo, sticker, game</code>"
    }

    async def client_ready(self, client, db):
        self.db = db
        self._client = client
        self.active_chats = set()

    @loader.command()
    async def sf(self, message):
        """<тип> - Запустить бесконечный фейк-статус"""
        args = utils.get_args_raw(message).lower()
        actions = {
            "typing": "typing",
            "voice": "record-audio",
            "video": "record-video",
            "photo": "upload-photo",
            "sticker": "choose-sticker",
            "game": "game"
        }

        if args not in actions:
            await utils.answer(message, self.strings["unknown"])
            return

        chat_id = message.chat_id
        if chat_id in self.active_chats:
            self.active_chats.remove(chat_id)
            await asyncio.sleep(0.5)

        self.active_chats.add(chat_id)
        await utils.answer(message, self.strings["started"].format(args))
        
        # Цикл имитации
        while chat_id in self.active_chats:
            try:
                async with message.client.action(chat_id, actions[args]):
                    await asyncio.sleep(4)
            except:
                break

    @loader.command()
    async def sfs(self, message):
        """Остановить фейк-статус"""
        if message.chat_id in self.active_chats:
            self.active_chats.remove(message.chat_id)
        await utils.answer(message, self.strings["stopped"])

    @loader.watcher(only_messages=True, only_mine=True)
    async def watcher(self, message):
        # Авто-стоп при отправке любого сообщения тобой
        if message.chat_id in self.active_chats and not message.text.startswith(".sf"):
            self.active_chats.remove(message.chat_id)