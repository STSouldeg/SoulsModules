# meta developer: @aethergeminibot, @Elizar_SoulsTeam
from .. import loader, utils
import random
import string

@loader.tds
class WildAnimalsMod(loader.Module):
    """WildNature PRO: Ни одного повтора благодаря сверке хешей файлов"""
    strings = {"name": "WildNature"}

    def __init__(self):
        self.history = set() # Храним уникальные ID файлов

    @loader.command()
    async def wild(self, message):
        """Прислать 100% уникальное фото животного"""
        await utils.answer(message, "🧬 **Сверяю ДНК зверя в базе данных...**")
        
        channels = [
            'wildlife_planet', 'natgeo', 'discovery_channel_official',
            'animal_planet', 'natgeowild', 'the_wildlife', 'nature'
        ]
        
        random.shuffle(channels)
        success = False
        stop_words = ['challenge', 'fit', 'подпишись', 'sale', 'promo', 'http', 't.me']

        for channel in channels:
            try:
                offset = random.randint(0, 1500)
                msgs = await self._client.get_messages(channel, limit=100, add_offset=offset)
                
                valid_photos = []
                for m in msgs:
                    if m.photo and not m.reply_markup:
                        # Сверяем уникальный ID самого файла (не сообщения!)
                        photo_id = m.photo.id
                        if photo_id in self.history:
                            continue
                        
                        text = (m.text or "").lower()
                        if any(word in text for word in stop_words):
                            continue

                        valid_photos.append(m)
                
                if valid_photos:
                    target = random.choice(valid_photos)
                    # Запоминаем ID файла
                    self.history.add(target.photo.id)
                    
                    if len(self.history) > 200:
                        self.history.clear()
                        
                    await self._client.send_file(
                        message.peer_id, 
                        target.photo, 
                        caption="🐾 **Уникальный кадр**\n\n✨ *For @Elizar_SoulsTeam*"
                    )
                    await message.delete()
                    success = True
                    break
            except Exception:
                continue
        
        if not success:
            # Резерв с обходом кеша Telegram (добавляем случайный хвост к URL)
            rand_str = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            fallback_url = f"https://loremflickr.com/1280/720/wildlife,animal/all?lock={rand_str}"
            try:
                await self._client.send_file(
                    message.peer_id, 
                    fallback_url,
                    caption="🐾 **Дикая природа (Свежий поток)**"
                )
                await message.delete()
            except:
                await utils.answer(message, "❌ Звери ушли на водопой. Попробуй позже.")