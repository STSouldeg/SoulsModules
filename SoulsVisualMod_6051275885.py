# meta developer: @Elizar_SoulsTeam
import asyncio
import random
from .. import loader, utils

@loader.tds
class SoulsVisualMod(loader.Module):
    """🎨 SoulsVisual: Стилизация и анимация твоего общения"""
    
    strings = {"name": "SoulsVisual 🎨"}

    @loader.command(ru_doc="<текст> - Эффект печатающейся машинки")
    async def typecmd(self, message):
        """Эффект живого набора текста"""
        text = utils.get_args_raw(message)
        if not text:
            await utils.answer(message, "❌ <b>Введите текст!</b>")
            return

        t_text = ""
        typing_symbol = "▒"
        
        for char in text:
            t_text += char
            await message.edit(f"<code>{t_text}{typing_symbol}</code>")
            await asyncio.sleep(0.1)
        
        await message.edit(f"<code>{t_text}</code>")

    @loader.command(ru_doc="<текст> - Глитч (Zalgo) эффект")
    async def glitchcmd(self, message):
        """Создать 'битый' текст"""
        text = utils.get_args_raw(message)
        if not text:
            await utils.answer(message, "❌ <b>Введите текст!</b>")
            return

        def zalgo(text):
            chars = [
                '\u030d', '\u030e', '\u0304', '\u0305', '\u033f', '\u0311', '\u0306', '\u0310', '\u0352', '\u033d', '\u0313', '\u0314', '\u0346', '\u034a', '\u034b', '\u034c', '\u0350', '\u0351', '\u0357', '\u0358', '\u0363', '\u0364', '\u0365', '\u0366', '\u0367', '\u0368', '\u0369', '\u036a', '\u036b', '\u036c', '\u036d', '\u036e', '\u036f', '\u0339', '\u033a', '\u033b', '\u033c', '\u0345', '\u0347', '\u0348', '\u0349', '\u034d', '\u034e', '\u0353', '\u0354', '\u0355', '\u0356', '\u0359', '\u035a', '\u0323', '\u0324', '\u0325', '\u0326', '\u0327', '\u0328', '\u032d', '\u032e', '\u0330', '\u0331', '\u0332', '\u0333', '\u033c', '\u0345', '\u0347', '\u0348', '\u0349', '\u034d', '\u034e', '\u0353', '\u0354', '\u0355', '\u0356', '\u0359', '\u035a', '\u0323', '\u0324', '\u0325', '\u0326', '\u0327', '\u0328', '\u032d', '\u032e', '\u0330', '\u0331', '\u0332', '\u0333'
            ]
            res = ""
            for char in text:
                res += char
                for _ in range(random.randint(2, 6)):
                    res += random.choice(chars)
            return res

        await message.edit(f"<code>{zalgo(text)}</code>")

    @loader.command(ru_doc="<текст> - Эффект дешифровки (Matrix)")
    async def matrixcmd(self, message):
        """Анимация расшифровки текста"""
        text = utils.get_args_raw(message)
        if not text:
            await utils.answer(message, "❌ <b>Введите текст!</b>")
            return

        symbols = "01$#%&@*§!?"
        final_text = list(text)
        current_display = [" " for _ in text]

        for i in range(len(text)):
            for _ in range(3): # Количество 'мерцаний' перед показом буквы
                current_display[i] = random.choice(symbols)
                await message.edit(f"<code>{''.join(current_display)}</code>")
                await asyncio.sleep(0.05)
            current_display[i] = final_text[i]
        
        await message.edit(f"<code>{text}</code>")

    @loader.command(ru_doc="<текст> - Переливающийся текст")
    async def magiccmd(self, message):
        """Магическая смена символов"""
        text = utils.get_args_raw(message)
        if not text: return
        
        frames = ["✨", "🌟", "💫", "💠"]
        for _ in range(5):
            await message.edit(f"{random.choice(frames)} <b>{text}</b> {random.choice(frames)}")
            await asyncio.sleep(0.3)
        await message.edit(f"✨ <b>{text}</b> ✨")