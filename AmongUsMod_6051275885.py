
from .. import loader, utils
import io
import aiohttp

@loader.tds
class AmongUsMod(loader.Module):
    """Among Us impostor generator"""
    strings = {"name": "AmongUs"}

    @loader.unrestricted
    async def amongcmd(self, message):
        """<text or reply> - Сгенерировать картинку Among Us"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        
        text = ""
        if args:
            text = args
        elif reply and reply.sender:
            user = await message.client.get_entity(reply.sender_id)
            text = f"{user.first_name} was an impostor."
        else:
            text = "Someone was an impostor."

        text = text.replace(" ", "%20")
        url = f"https://vacefron.nl/api/amongus?text={text}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    await utils.answer(message, "Ошибка API")
                    return
                data = await resp.read()

        file = io.BytesIO(data)
        file.name = "impostor.png"
        file.seek(0)

        await utils.answer(message, file=file)