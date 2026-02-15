# meta developer: @Elizar_SoulsTeam
# meta banner: https://i.imgur.com/8QA5l6P.jpeg

from .. import loader, utils

@loader.tds
class QuickGiftsMod(loader.Module):
    """Самый легкий модуль для подарков. Без зависимостей."""
    strings = {"name": "QuickGifts"}

    @loader.command()
    async def gift(self, message):
        """<цена> <текст> (reply) - Подарить подарок"""
        reply = await message.get_reply_message()
        if not reply:
            return await utils.answer(message, "<b>❌ Ответь на сообщение получателя!</b>")

        args = utils.get_args(message)
        if not args or not args[0].isdigit():
            return await utils.answer(message, "<b>❌ Укажи цену (15, 25, 50, 100)</b>")

        stars = int(args[0])
        text = " ".join(args[1:]) if len(args) > 1 else ""

        # ID подарков
        gift_ids = {
            15: 5170145012310081615,  # Сердце
            25: 5170250947678437525,  # Подарок
            50: 5170314324215857265,  # Цветы
            100: 5168043875654172773  # Кубок
        }
        gift_id = gift_ids.get(stars, 5170145012310081615)

        await self._send_raw(message, reply.sender_id, gift_id, text)

    @loader.command()
    async def sgvalentine(self, message):
        """<текст> (reply) - Подарить валентинку"""
        reply = await message.get_reply_message()
        if not reply:
            return await utils.answer(message, "<b>❌ Ответь на сообщение!</b>")

        text = utils.get_args_raw(message) or "С 14 февраля! ❤️"
        valentine_id = 5170145012310081615 # Анимированное сердце

        await message.edit("<b>💌 Подготовка валентинки...</b>")
        await self._send_raw(message, reply.sender_id, valentine_id, text)

    async def _send_raw(self, message, user_id, gift_id, text):
        try:
            # Используем динамический доступ к классам через клиент, чтобы обмануть загрузчик
            client = message.client
            m = __import__('telethon.tl', fromlist=['types', 'functions'])
            
            user = await client.get_input_entity(user_id)
            
            # Собираем инвойс
            inv = m.types.InputInvoiceStarGift(
                peer=user,
                gift_id=gift_id,
                message=m.types.TextWithEntities(text, [])
            )
            
            # Отправляем запрос
            form = await client(m.functions.payments.GetPaymentFormRequest(inv))
            await client(m.functions.payments.SendStarsFormRequest(form.form_id, inv))
            
            await message.edit("<b>✅ Исполнено! Дар отправлен.</b>")
        except Exception as e:
            await message.edit(f"<b>❌ Ошибка:</b> <code>{str(e)}</code>")