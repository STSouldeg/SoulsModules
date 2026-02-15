# meta developer: @Elizar_SoulsTeam
# requires: aiohttp

import aiohttp
from .. import loader, utils

@loader.tds
class SoulsWeatherMod(loader.Module):
    """🌤 SoulsWeather: Прогноз погоды для твоего набора"""
    
    strings = {"name": "SoulsWeather 🌤"}

    @loader.command(ru_doc="<город> - Узнать погоду")
    async def wcmd(self, message):
        """Узнать погоду в указанном городе"""
        args = utils.get_args_raw(message)
        city = args if args else "Москва"
        
        status = await utils.answer(message, f"📡 <b>Запрашиваю метеоданные для:</b> <code>{city}</code>...")

        async with aiohttp.ClientSession() as session:
            try:
                # Запрос к wttr.in в формате JSON
                async with session.get(f"https://wttr.in/{city}?format=j1&lang=ru") as resp:
                    if resp.status != 200:
                        await status.edit("❌ <b>Город не найден или сервис недоступен.</b>")
                        return
                    
                    data = await resp.json()
                    curr = data['current_condition'][0]
                    area = data['nearest_area'][0]
                    
                    temp = curr['temp_C']
                    feels = curr['FeelsLikeC']
                    desc = curr['lang_ru'][0]['value']
                    hum = curr['humidity']
                    wind = curr['windspeedKmph']
                    city_name = area['areaName'][0]['value']
                    country = area['country'][0]['value']

                    # Подбор эмодзи по описанию
                    icon = "☀️"
                    d_lower = desc.lower()
                    if "облачно" in d_lower or "пасмурно" in d_lower: icon = "☁️"
                    elif "дождь" in d_lower: icon = "🌧"
                    elif "снег" in d_lower: icon = "❄️"
                    elif "гроза" in d_lower: icon = "⛈"
                    elif "туман" in d_lower: icon = "🌫"

                    res = f"<b>ПОГОДА В:</b> <code>{city_name}, {country}</code>\n"
                    res += "━━━━━━━━━━━━━━━━━━━━\n"
                    res += f"{icon} <b>СОСТОЯНИЕ:</b> <code>{desc.capitalize()}</code>\n"
                    res += f"🌡 <b>ТЕМПЕРАТУРА:</b> <code>{temp}°C</code>\n"
                    res += f"🤔 <b>ОЩУЩАЕТСЯ:</b> <code>{feels}°C</code>\n"
                    res += f"💧 <b>ВЛАЖНОСТЬ:</b> <code>{hum}%</code>\n"
                    res += f"💨 <b>ВЕТЕР:</b> <code>{wind} км/ч</code>\n"
                    res += "━━━━━━━━━━━━━━━━━━━━"
                    
                    await status.edit(res)
            except Exception as e:
                await status.edit(f"❌ <b>Ошибка:</b> <code>{str(e)}</code>")