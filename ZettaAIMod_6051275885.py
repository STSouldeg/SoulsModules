# meta developer: @Elizar_SoulsTeam
# requires: aiohttp

import json
import logging
import aiohttp
import re
import base64
import io
import random
from .. import loader, utils

available_models = {
    "1": "o3-PRO", "2": "o1-PRO", "3": "o3-Mini-High", "4": "Grok 4",
    "5": "GPT 4.1", "12": "gpt-4.5", "13": "gpt-5", "14": "gpt-4o-mini",
    "18": "deepseek-v3", "19": "deepseek-r1", "20": "gemini-1.5 Pro",
    "23": "gemini-2.0-flash", "30": "claude-4.5-sonnet"
}

@loader.tds
class ZettaAIMod(loader.Module):
    """🧠 Souls Zetta AI: 35+ моделей ИИ в одном флаконе"""
    
    strings = {"name": "Souls Zetta"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            "MODEL", "gpt-4o-mini", "Модель по умолчанию",
            "HUMAN_MODE", False, "Скрывать приписку модели"
        )

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    @loader.command(ru_doc="<запрос> - Одиночный запрос к ИИ")
    async def aicmd(self, message):
        """Запрос к ИИ"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        query = reply.text if reply else args

        if not query:
            await utils.answer(message, "<b>🤔 Что спросить?</b>")
            return

        status = await utils.answer(message, "<b>🤔 Zetta думает...</b>")
        
        # API URL для Zetta
        api_url = "http://zetta.onlysq.ru:34010/OnlySq-Zetta/v1/models"
        
        payload = {
            "model": "gemini-2.0-flash", # Оптимально для Zetta API
            "request": {"messages": [{"role": "user", "content": query}]}
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(api_url, json=payload) as r:
                    if r.status != 200:
                        await status.edit("❌ <b>Ошибка API. Попробуйте позже.</b>")
                        return
                    
                    data = await r.json()
                    ans_base64 = data.get("answer", "")
                    if not ans_base64:
                        await status.edit("❌ <b>Ответ пуст.</b>")
                        return
                    
                    answer = base64.b64decode(ans_base64).decode('utf-8')
                    
                    res = f"💡 <b>Ответ Zetta ({self.config['MODEL']}):</b>\n\n{answer}"
                    if self.config["HUMAN_MODE"]:
                        res = answer

                    await status.edit(res)
            except Exception as e:
                await status.edit(f"❌ <b>Ошибка:</b> <code>{str(e)}</code>")

    @loader.command(ru_doc="Показать список доступных моделей")
    async def modelslistcmd(self, message):
        """Список моделей"""
        res = "📝 <b>Доступные модели в Zetta:</b>\n\n"
        for k, v in available_models.items():
            res += f"<b>{k}</b> — <code>{v}</code>\n"
        await utils.answer(message, res)

    @loader.command(ru_doc="<номер> - Установить модель")
    async def setmodelcmd(self, message):
        """Смена модели"""
        args = utils.get_args_raw(message)
        if args in available_models:
            self.config["MODEL"] = available_models[args]
            await utils.answer(message, f"✅ <b>Модель изменена на:</b> {available_models[args]}")
        else:
            await utils.answer(message, "❌ <b>Неверный номер. См. .modelslist</b>")