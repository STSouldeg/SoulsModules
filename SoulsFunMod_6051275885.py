# meta developer: @Elizar_SoulsTeam
# requires: aiohttp

import asyncio
import random
import aiohttp
import io
from .. import loader, utils

@loader.tds
class SoulsFunMod(loader.Module):
    """🤡 SoulsFun: Троллинг, Анимации и Озвучка текста"""
    
    strings = {"name": "SoulsFun 🤡"}

    @loader.command(ru_doc="- Анимация сердца")
    async def heartcmd(self, message):
        """Построить анимированное сердце"""
        heart_frames = [
            "❤️", "🖤❤️🖤", "❤️🖤❤️🖤❤️", "❤️🖤❤️🖤❤️", "🖤❤️🖤❤️🖤", "🖤🖤❤️🖤🖤", "🖤🖤🖤"
        ]
        res = ""
        for frame in heart_frames:
            res += frame + "\n"
            await message.edit(f"<b>{res}</b>")
            await asyncio.sleep(0.3)

    @loader.command(ru_doc="- Текстовая бомба")
    async def bombcmd(self, message):
        """Запустить обратный отсчет"""
        for i in range(3, 0, -1):
            await message.edit(f"💣 <b>До взрыва: {i}...</b>")
            await asyncio.sleep(1)
        await message.edit("💥 <b>БА-БАХ!</b>")

    @loader.command(ru_doc="<typing|record_audio|playing> - Фейковое действие")
    async def fapicmd(self, message):
        """Включить статус 'печатает' или 'записывает ГС'"""
        args = utils.get_args_raw(message)
        action = args if args in ["typing", "record_audio", "playing"] else "typing"
        
        await message.edit(f"🎭 <b>Статус '{action}' включен на 30 секунд...</b>")
        
        for _ in range(6): # 6 циклов по 5 секунд
            async with message.client.action(message.chat_id, action):
                await asyncio.sleep(5)
        
        await message.edit("✅ <b>Действие завершено.</b>")

    @loader.command(ru_doc="<текст> - Озвучить текст и отправить как ГС")
    async def saycmd(self, message):
        """Превратить текст в голосовое сообщение (TTS)"""
        text = utils.get_args_raw(message)
        if not text:
            # Если текста нет, пробуем взять из реплая
            reply = await message.get_reply_message()
            if reply and reply.text:
                text = reply.text
            else:
                await utils.answer(message, "❌ <b>Введите текст или ответьте на сообщение!</b>")
                return

        await message.edit("🎙 <b>Записываю голосовое...</b>")
        
        # Google TTS API (неофициальное, но рабочее)
        tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={text.replace(' ', '%20')}&tl=ru&client=tw-ob"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(tts_url) as resp:
                    if resp.status == 200:
                        audio_data = await resp.read()
                        f = io.BytesIO(audio_data)
                        f.name = "voice.ogg"
                        await message.client.send_file(message.chat_id, f, voice_note=True)
                        await message.delete()
                    else:
                        await message.edit("❌ <b>Ошибка сервиса озвучки.</b>")
            except Exception as e:
                await message.edit(f"❌ <b>Ошибка:</b> <code>{str(e)}</code>")