# meta developer: @Elizar_SoulsTeam
# meta banner: https://i.imgur.com/8QA5l6P.jpeg

from .. import loader, utils
from telethon import types, functions
import struct

@loader.tds
class StarSenderMod(loader.Module):
    """Официальные подарки за Звезды (Deep Injection Edition)"""
    strings = {"name": "StarSender"}

    async def client_ready(self, client, db):
        self._client = client
        # Попытка поднять слой протокола в памяти
        try:
            if hasattr(self._client, 'session'):
                self._client.session.layer = 189
        except: pass

    def _get_raw_invoice(self, peer, gift_id, message_text):
        """Ручная сборка бинарного пакета InputInvoiceStarGift"""
        # Конструктор TextWithEntities (0x751f1111)
        # Мы делаем пустой список сущностей для стабильности
        text_bytes = self._encode_string(message_text)
        entities_bytes = struct.pack('<Ii', 0x1cb5c415, 0) # Vector ID + count 0
        text_with_entities = struct.pack('<I', 0x751f1111) + text_bytes + entities_bytes
        
        # Конструктор InputInvoiceStarGift (0x323c91f5)
        # flags (4) + peer (var) + gift_id (8) + message (var)
        flags = 0
        data = struct.pack('<I I', 0x323c91f5, flags)
        data += peer._bytes()
        data += struct.pack('<q', gift_id)
        data += text_with_entities
        return data

    def _encode_string(self, s):
        """Правильное кодирование строк для Telegram TL"""
        b = s.encode('utf-8')
        if len(b) <= 253:
            return bytes([len(b)]) + b + b'\x00' * (-(len(b) + 1) % 4)
        else:
            return b'\xfe' + struct.pack('<I', len(b))[:3] + b + b'\x00' * (-len(b) % 4)

    @loader.command()
    async def tgift(self, message):
        """<цена> <текст> (reply) - Реальный подарок через сырой протокол"""
        reply = await message.get_reply_message()
        if not reply:
            return await utils.answer(message, "<b>❌ Репли на того, кому даришь!</b>")

        args = utils.get_args(message)
        if not args or not args[0].isdigit():
            return await utils.answer(message, "<b>❌ Укажи цену (15, 25, 50...)</b>")

        stars = int(args[0])
        text = " ".join(args[1:]) if len(args) > 1 else ""

        gift_ids = {
            15: 5170145012310081615, 25: 5170250947678437525, 
            50: 5170314324215857265, 100: 5168043875654172773
        }
        gift_id = gift_ids.get(stars, 5170250947678437525)

        try:
            # Обновляем слой перед запросом
            self._client.session.layer = 189
            
            user_peer = await self._client.get_input_entity(reply.sender_id)
            
            # Создаем фейковый объект с нужным методом _bytes
            class SyntheticInvoice:
                def __init__(self, data): self.data = data
                def _bytes(self): return self.data
                def to_dict(self): return {}

            raw_data = self._get_raw_invoice(user_peer, gift_id, text)
            synthetic = SyntheticInvoice(raw_data)

            # Вызываем GetPaymentFormRequest напрямую
            # payments.getPaymentForm#37135e69 invoice:InputInvoice = payments.PaymentForm
            form = await self._client(functions.payments.GetPaymentFormRequest(invoice=synthetic))
            
            #payments.sendStarsForm#339178d4 form_id:long invoice:InputInvoice = payments.PaymentResult
            class SyntheticSendRequest(functions.TLRequest):
                CONSTRUCTOR_ID = 0x339178d4
                def __init__(self, f_id, inv):
                    self.f_id = f_id
                    self.inv = inv
                def _bytes(self):
                    return struct.pack('<Iq', 0x339178d4, self.f_id) + self.inv._bytes()

            await self._client(SyntheticSendRequest(form.form_id, synthetic))
            await message.edit("<b>Подарок доставлен! ❤️</b>")

        except Exception as e:
            if "323C91F5" in str(e):
                await message.edit("<b>❌ Сервер всё еще отклоняет старый протокол.</b>\n<i>Без обновления ядра (.upcore) официальные подарки не пройдут.</i>")
            else:
                await message.edit(f"<b>❌ Ошибка:</b> <code>{str(e)}</code>")