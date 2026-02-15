# meta developer: @Elizar_SoulsTeam
# meta banner: https://i.imgur.com/8QA5l6P.jpeg

from .. import loader, utils
import asyncio

@loader.tds
class SoulGiftsMod(loader.Module):
    """Шикарные визуальные подарки и валентинки (Soul Style)"""
    strings = {"name": "SoulGifts"}

    @loader.command()
    async def gift(self, message):
        """<текст> (reply) - Подарить анимированный подарок"""
        reply = await message.get_reply_message()
        text = utils.get_args_raw(message) or "Твой особенный подарок!"
        
        target = f"для {reply.sender.first_name}" if reply else "для тебя"
        
        # Анимация распаковки
        frames = ["📦", "🎁", "✨🎁✨", "🎊🎁🎊", "🎇"]
        for frame in frames:
            await message.edit(f"<b>{frame}</b>")
            await asyncio.sleep(0.4)
        
        res = (
            f"<b>🎁 ПОДАРОК {target.upper()}</b>\n"
            f"<b>━━━━━━━━━━━━━━</b>\n"
            f"<b>💎 Содержимое:</b> <code>{text}</code>\n"
            f"<b>━━━━━━━━━━━━━━</b>\n"
            f"✨ <i>Отправлено через SoulGifts</i>"
        )
        await message.edit(res)

    @loader.command()
    async def sgvalentine(self, message):
        """<текст> (reply) - Отправить валентинку (14 февраля)"""
        reply = await message.get_reply_message()
        text = utils.get_args_raw(message) or "Я тебя люблю! ❤️"
        
        name = reply.sender.first_name if reply else "тебе"

        # Красивая анимация письма
        await message.edit("💌 <code>Sending Love...</code>")
        await asyncio.sleep(0.5)
        await message.edit("📩 <code>Opening...</code>")
        await asyncio.sleep(0.5)
        
        valentine = (
            f"<b>╭━━━ ❤️ VALENTINE ❤️ ━━━╮</b>\n"
            f"<b>┃</b>\n"
            f"<b>┃  Дорогой(ая) {name},</b>\n"
            f"<b>┃  {text}</b>\n"
            f"<b>┃</b>\n"
            f"<b>╰━━━━━━━━━━━━━━━━━━━━╯</b>\n"
            f"       ❤️🌹❤️🌹❤️🌹❤️"
        )
        await message.edit(valentine)