# meta developer: @Elizar_SoulsTeam
# meta banner: https://i.imgur.com/8QA5l6P.jpeg

from .. import loader, utils
import os

@loader.tds
class SoulBypassMod(loader.Module):
    """Модуль для обхода запретов и подмены медиа."""
    strings = {"name": "SoulBypass"}

    @loader.command()
    async def copy(self, message):
        """(reply) - Копировать запрещенку (фото, видео, текст)"""
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, "<b>❌ Ответь на пост!</b>")
            return

        await utils.answer(message, "<b>📥 Обхожу защиту...</b>")
        
        if reply.media:
            path = await reply.download_media()
            await message.client.send_file("me", path, caption=reply.text)
            await message.client.send_file(message.chat_id, path, caption=reply.text)
            if os.path.exists(path):
                os.remove(path)
        else:
            await message.client.send_message("me", reply.text)
            await message.client.send_message(message.chat_id, reply.text)
        
        await message.delete()

    @loader.command()
    async def vmsg(self, message):
        """(reply) - Аудио -> Голосовое"""
        reply = await message.get_reply_message()
        if not reply or not (reply.audio or reply.voice or reply.document):
            await utils.answer(message, "<b>❌ Ответь на аудиофайл!</b>")
            return

        await utils.answer(message, "<b>🎙 Конвертирую в ГС...</b>")
        path = await reply.download_media()
        await message.delete()
        await message.client.send_file(message.chat_id, path, voice_note=True, reply_to=reply.reply_to_msg_id)
        if os.path.exists(path):
            os.remove(path)

    @loader.command()
    async def vnote(self, message):
        """(reply) - Видео -> Кружочек"""
        reply = await message.get_reply_message()
        if not reply or not (reply.video or reply.document):
            await utils.answer(message, "<b>❌ Ответь на видео!</b>")
            return

        await utils.answer(message, "<b>📹 Конвертирую в кружок...</b>")
        path = await reply.download_media()
        await message.delete()
        try:
            await message.client.send_file(message.chat_id, path, video_note=True, reply_to=reply.reply_to_msg_id)
        except:
            await message.client.send_message(message.chat_id, "<b>❌ Ошибка: видео должно быть квадратным!</b>")
        
        if os.path.exists(path):
            os.remove(path)