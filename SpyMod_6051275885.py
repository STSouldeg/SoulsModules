
from .. import loader, utils
from telethon.tl.types import Message

@loader.tds
class SpyMod(loader.Module):
    """Следит за изменениями сообщений (AntiEdit)"""
    strings = {"name": "Spy"}

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        if not self.get("messages", False):
            self.set("messages", {})

    @loader.watcher(only_messages=True, out=False)
    async def watcher(self, message):
        if not isinstance(message, Message) or not message.text:
            return
        
        msgs = self.get("messages", {})
        msgs[str(message.id)] = message.text
        # Храним последние 100 сообщений, чтобы не забивать память
        if len(msgs) > 100:
            keys = list(msgs.keys())
            del msgs[keys[0]]
        self.set("messages", msgs)

    async def client_ready(self, client, db):
        self.db = db

    @loader.watcher(only_messages=True, out=False, only_media=False)
    async def edit_watcher(self, message):
        if not message.edit_date:
            return
            
        msgs = self.get("messages", {})
        old_text = msgs.get(str(message.id))
        
        if old_text and old_text != message.text:
            await message.reply(f"👀 <b>Замечено изменение!</b>\n\n<b>Было:</b>\n<code>{old_text}</code>\n\n<b>Стало:</b>\n<code>{message.text}</code>")
            msgs[str(message.id)] = message.text
            self.set("messages", msgs)