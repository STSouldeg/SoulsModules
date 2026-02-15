# meta developer: @Elizar_SoulsTeam
import subprocess
import json
from .. import loader, utils

@loader.tds
class SoulsMailMod(loader.Module):
    """📧 SoulsMail: Временная почта (CURL Edition)
    Работает даже если в Термуксе сломан asyncio/aiohttp"""
    strings = {"name": "SoulsMail"}

    async def client_ready(self, client, db):
        self.db = db
        self.api = "https://www.1secmail.com/api/v1/"

    def _curl(self, url):
        """Прямой запрос через системный curl"""
        try:
            result = subprocess.run(["curl", "-L", "-s", url], capture_output=True, text=True)
            return json.loads(result.stdout)
        except Exception as error:
            return {"error": str(error)}

    @loader.command(ru_doc="Создать новую почту")
    async def secmailcmd(self, message):
        """Сгенерировать почту через CURL"""
        await utils.answer(message, "⏳ <b>Пробиваю канал через CURL...</b>")
        
        url = f"{self.api}?action=genRandomMailbox&count=1"
        data = self._curl(url)
        
        if isinstance(data, dict) and "error" in data:
            return await utils.answer(message, f"❌ <b>Ошибка:</b> {data['error']}")
        
        email = data[0]
        self.db.set("SoulsMail", "email", email)
        await utils.answer(message, f"📬 <b>Твоя почта:</b>\n<code>{email}</code>\n\n<i>Проверка: .seclist</i>")

    @loader.command(ru_doc="Проверить входящие")
    async def seclistcmd(self, message):
        """Проверить входящие через CURL"""
        email = self.db.get("SoulsMail", "email")
        if not email:
            return await utils.answer(message, "❌ <b>Сначала создай почту!</b>")

        await utils.answer(message, "⏳ <b>Чекаю письма...</b>")
        login, domain = email.split("@")
        url = f"{self.api}?action=getMessages&login={login}&domain={domain}"
        data = self._curl(url)
        
        if not data:
            return await utils.answer(message, "📩 <b>Писем нет.</b>")
        
        res = "📥 <b>Входящие:</b>\n\n"
        for m in data:
            res += f"🆔 <code>{m['id']}</code> | <b>От:</b> {m['from']}\n<b>Тема:</b> {m['subject']}\n"
        await utils.answer(message, res)

    @loader.command(ru_doc="Прочитать письмо по ID")
    async def secgetcmd(self, message):
        """Прочитать письмо через CURL"""
        args = utils.get_args_raw(message)
        email = self.db.get("SoulsMail", "email")
        if not args or not args.isdigit() or not email:
            return await utils.answer(message, "❌ <b>Ошибка в ID или почта не создана.</b>")

        login, domain = email.split("@")
        url = f"{self.api}?action=readMessage&login={login}&domain={domain}&id={args}"
        data = self._curl(url)
        
        res = (
            f"📧 <b>От:</b> {data['from']}\n"
            f"📝 <b>Тема:</b> {data['subject']}\n"
            f"━━━━━━━━━━━━━━━\n"
            f"<code>{data['textBody']}</code>"
        )
        await utils.answer(message, res)