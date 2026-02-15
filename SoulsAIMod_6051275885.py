# meta developer: @Elizar_SoulsTeam
# requires: aiohttp

import json
import os
import aiohttp
import re
from .. import loader, utils

@loader.tds
class SoulsAIMod(loader.Module):
    """AI-помощник по Hikka (Souls Edition)"""
    
    strings = {"name": "Souls AI"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            "PROVIDER", "onlysq", "Провайдер API (onlysq или devj)",
            "METOD", "off", "Качественный ответ (on/off)"
        )

    async def client_ready(self, client, db):
        self.client = client

    @loader.command(ru_doc="<запрос> - Спросить ИИ")
    async def aisupcmd(self, message):
        """Спросить ИИ-помощника"""
        await self._process(message, "https://raw.githubusercontent.com/Chaek1403/VAWEIRR/refs/heads/main/instruction.txt")

    @loader.command(ru_doc="<запрос> - Спросить ИИ про ошибку")
    async def aierrorcmd(self, message):
        """Помощь с ошибками"""
        await self._process(message, "https://raw.githubusercontent.com/Chaek1403/VAWEIRR/refs/heads/main/error_instruction.txt")

    async def _process(self, message, instr_url):
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        query = reply.text if reply else args

        if not query:
            await utils.answer(message, "<b>🤔 О чем спросить?</b>")
            return

        status = await utils.answer(message, "<b>🤔 Думаю...</b>")

        async with aiohttp.ClientSession() as session:
            try:
                # Качаем инструкцию
                async with session.get(instr_url) as resp:
                    instr = await resp.text()

                # Запрос к API
                provider = self.config["PROVIDER"]
                if provider == "devj":
                    api_url = "https://api.vysssotsky.ru/v1/chat/completions"
                    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"}
                    payload = {
                        "model": "gpt-4",
                        "messages": [{"role": "user", "content": f"{instr}\n\nЗапрос: {query}"}]
                    }
                    async with session.post(api_url, headers=headers, json=payload) as r:
                        data = await r.json()
                        ans = data['choices'][0]['message']['content']
                else:
                    api_url = "http://api.onlysq.ru/ai/v2"
                    payload = {
                        "model": "gpt-3.5-turbo",
                        "request": {"messages": [{"role": "user", "content": f"{instr}\n\nЗапрос: {query}"}]}
                    }
                    async with session.post(api_url, json=payload) as r:
                        data = await r.json()
                        ans = data.get("answer", "🚫 Нет ответа")

                await status.edit(f"💡 <b>Souls AI:</b>\n\n{ans}")
            except Exception as e:
                await status.edit(f"❌ <b>Ошибка:</b> <code>{str(e)}</code>")

    @loader.command(ru_doc="onlysq/devj - Сменить провайдера")
    async def aiprovcmd(self, message):
        """Смена провайдера"""
        args = utils.get_args_raw(message)
        if args in ["onlysq", "devj"]:
            self.config["PROVIDER"] = args
            await utils.answer(message, f"✅ Провайдер изменен на <b>{args}</b>")
        else:
            await utils.answer(message, "❌ Укажите <code>onlysq</code> или <code>devj</code>")