import random
import requests
from datetime import datetime
import pytz
from hikkatl.types import Message
from .. import loader, utils

@loader.tds
class UltimateCosmoMod(loader.Module):
    """Полный космический модуль с русскими переводами"""  
    strings = {
        "name": "CosmoProRU",
        "fact": "🔭 <b>Космический факт:</b>\n<code>{}</code>",
        "iss": (
            "🛰 <b>Местоположение МКС:</b>\n"
            "→ Широта: <code>{lat}</code>\n"
            "→ Долгота: <code>{lon}</code>\n\n"
            "<a href='https://maps.google.com/?q={lat},{lon}'>🗺 Открыть на карте</a>"
        ),
        "mars": (
            "🌡 <b>Погода на Марсе (Сол {sol}):</b>\n"
            "→ Температура: <code>{temp}°C</code>\n"
            "→ Давление: <code>{pressure} Па</code>\n"
            "→ Ветер: <code>{wind} м/с</code>"
        ),
        "nick": "🚀 <b>Твой космический ник:</b> <code>{}</code>",
        "launch": (
            "🚀 <b>Ближайший запуск ракеты:</b>\n"
            "→ Миссия: <code>{name}</code>\n"
            "→ Дата: <code>{date}</code>\n"
            "→ Космодром: <code>{location}</code>"
        ),
        "apod": (
            "🚀 <b>Фото дня от NASA</b>\n\n"
            "<b>Название:</b> <code>{title}</code>\n"
            "📅 <b>Дата:</b> <code>{date}</code>\n"
            "📌 <b>Тип:</b> {media_type}\n\n"
            "<b>Описание:</b>\n{explanation}"
        ),
        "galaxy": (
            "🌌 <b>Галактика:</b> <code>{name}</code>\n"
            "📏 <b>Тип:</b> {type}\n"
            "🪐 <b>Известные планеты:</b>\n{planets}"
        ),
        "planet": (
            "🪐 <b>Планета {name}:</b>\n"
            "📏 <b>Тип:</b> {type}\n"
            "⚖️ <b>Масса:</b> {mass}\n"
            "📐 <b>Диаметр:</b> {diameter}\n"
            "🌡 <b>Температура:</b> {temp}\n"
            "📜 <b>Интересное:</b> {info}"
        ),
        "error": "❌ Ошибка: {}",
        "no_args": "ℹ️ Доступные объекты:\n{}"
    }

    def __init__(self):
        self.galaxies = {
            "Млечный Путь": {
                "type": "Спиральная галактика",
                "planets": [
                    "Меркурий", "Венера", "Земля", "Марс",
                    "Юпитер", "Сатурн", "Уран", "Нептун"
                ]
            },
            "Андромеда": {
                "type": "Спиральная галактика",
                "planets": ["Андромеда b", "Андромеда c", "Андромеда d"]
            }
        }

        self.planets = {
            "Меркурий": {
                "type": "Терраподобная",
                "mass": "3.3 × 10²³ кг",
                "diameter": "4 880 км",
                "temp": "-173°C до 427°C",
                "info": "Самая маленькая планета Солнечной системы"
            },
            "Венера": {
                "type": "Терраподобная",
                "mass": "4.87 × 10²⁴ кг",
                "diameter": "12 104 км",
                "temp": "462°C (средняя)",
                "info": "Самый горячий мир в Солнечной системе"
            },
            "Земля": {
                "type": "Терраподобная",
                "mass": "5.97 × 10²⁴ кг",
                "diameter": "12 742 км",
                "temp": "-89°C до 58°C",
                "info": "Единственная известная обитаемая планета"
            },
            "Марс": {
                "type": "Терраподобная",
                "mass": "6.39 × 10²³ кг",
                "diameter": "6 779 км",
                "temp": "-153°C до 20°C",
                "info": "Красная планета с самой высокой горой Олимп"
            },
            "Юпитер": {
                "type": "Газовый гигант",
                "mass": "1.9 × 10²⁷ кг",
                "diameter": "139 820 км",
                "temp": "-108°C (верхние слои)",
                "info": "Самый большой шторм (Большое красное пятно)"
            },
            "Сатурн": {
                "type": "Газовый гигант",
                "mass": "5.68 × 10²⁶ кг",
                "diameter": "116 460 км",
                "temp": "-139°C (верхние слои)",
                "info": "Имеет самые заметные кольца"
            },
            "Уран": {
                "type": "Ледяной гигант",
                "mass": "8.68 × 10²⁵ кг",
                "diameter": "50 724 км",
                "temp": "-197°C (верхние слои)",
                "info": "Вращается на боку (98° наклон)"
            },
            "Нептун": {
                "type": "Ледяной гигант",
                "mass": "1.02 × 10²⁶ кг",
                "diameter": "49 244 км",
                "temp": "-201°C (верхние слои)",
                "info": "Самые сильные ветра (до 2100 км/ч)"
            }
        }

        self.apod_translations = {
            "Planet Lines Across Water": "Линии планет на воде",
            "What's causing those lines?": "Что вызывает эти линии?",
            "Objects in the sky sometimes appear reflected as lines across water": 
                "Объекты в небе иногда отражаются в виде линий на воде",
            "If the water's surface is smooth": 
                "Если поверхность воды гладкая",
            "then reflected objects would appear similarly": 
                "то отраженные объекты выглядят как обычные пятна",
            "But if the water is choppy": 
                "Но если вода неспокойная",
            "there are many places where light from the object can reflect": 
                "свет от объекта отражается во многих точках",
            "The same effect is frequently seen for the Sun": 
                "Такой же эффект часто наблюдается с Солнцем",
            "Pictured about 10 days ago in Ibiza, Spain": 
                "Снято 10 дней назад на Ибице, Испания",
            "images of the setting Moon, Venus (top), and Saturn (right, faint)": 
                "изображения заходящей Луны, Венеры (вверху) и Сатурна (справа, слабо)",
            "The other bright object on the right with a water-reflected line is a beacon": 
                "Другой яркий объект справа с отражением - это маяк",
            "Explore Your Universe: Random APOD Generator": 
                "Исследуй Вселенную: Генератор случайных APOD"
        }

    async def translate_apod(self, text):
        """Переводит основные фразы из описания APOD"""
        for eng, ru in self.apod_translations.items():
            text = text.replace(eng, ru)
        return text

    async def client_ready(self, client, db):
        self.client = client

    async def factcmd(self, message: Message):
        """Случайный факт о космосе"""
        facts = [
            "Диаметр Марса - примерно половина Земли.",
            "Один день на Венере длиннее, чем её год.",
            "Солнечному свету нужно 8 минут, чтобы достичь Земли.",
            "МКС движется со скоростью 27 600 км/ч.",
            "На Луне есть мусор от миссий Apollo."
        ]
        await utils.answer(message, self.strings["fact"].format(random.choice(facts)))

    async def isscmd(self, message: Message):
        """Текущее положение МКС"""
        try:
            data = requests.get("http://api.open-notify.org/iss-now.json").json()
            await utils.answer(
                message,
                self.strings["iss"].format(
                    lat=data["iss_position"]["latitude"],
                    lon=data["iss_position"]["longitude"]
                )
            )
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))

    async def marscmd(self, message: Message):
        """Погода на Марсе"""
        try:
            data = requests.get(
                "https://api.nasa.gov/insight_weather/?api_key=DEMO_KEY&feedtype=json&ver=1.0"
            ).json()
            sol = list(data["sol_keys"])[-1]
            weather = data[sol]
            await utils.answer(
                message,
                self.strings["mars"].format(
                    sol=sol,
                    temp=weather['AT']['av'],
                    pressure=weather['PRE']['av'],
                    wind=weather['HWS']['av']
                )
            )
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))

    async def nickcmd(self, message: Message):
        """Генератор космических ников"""
        parts = [
            ["Космо", "Астро", "Галакти", "Орбита", "Нептун"],
            ["навт", "зонд", "путешественник", "исследователь", "странник"]
        ]
        nick = random.choice(parts[0]) + random.choice(parts[1])
        await utils.answer(message, self.strings["nick"].format(nick))

    async def launchcmd(self, message: Message):
        """Ближайший запуск ракеты"""
        try:
            data = requests.get("https://lldev.thespacedevs.com/2.2.0/launch/upcoming/?limit=1").json()
            launch = data["results"][0]
            
            # Перевод названия миссии
            name_trans = {
                "Long March 12": "Чанчжэн-12",
                "SatNet LEO Group": "Группа спутников SatNet",
                "Wenchang Space Launch Site": "Космодром Вэньчан"
            }
            
            name = launch['name']
            for eng, ru in name_trans.items():
                name = name.replace(eng, ru)
            
            dt = datetime.strptime(launch["net"], "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=pytz.utc
            )
            
            location = launch['pad']['location']['name']
            for eng, ru in name_trans.items():
                location = location.replace(eng, ru)
            
            await utils.answer(
                message,
                self.strings["launch"].format(
                    name=name,
                    date=dt.strftime('%d.%m.%Y %H:%M'),
                    location=location
                )
            )
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))

    async def apodcmd(self, message: Message):
        """Фото дня от NASA с переводом"""
        try:
            data = requests.get(
                "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
            ).json()
            
            media_type = "📹 Видео" if data["media_type"] == "video" else "🖼 Фото"
            explanation = await self.translate_apod(data.get('explanation', 'Описание отсутствует'))
            
            title = data['title']
            for eng, ru in self.apod_translations.items():
                title = title.replace(eng, ru)
            
            await message.client.send_file(
                message.chat_id,
                data["url"],
                caption=self.strings["apod"].format(
                    title=title,
                    date=data['date'],
                    media_type=media_type,
                    explanation=explanation
                ),
                reply_to=message.id,
            )
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))

    async def galaxycmd(self, message: Message):
        """Информация о галактике"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(
                message,
                self.strings["no_args"].format(
                    "\n".join([f"• <code>{g}</code>" for g in self.galaxies.keys()])
                ) + "\n\nИспользуйте: <code>.galaxy [название]</code>"
            )
            return

        if args not in self.galaxies:
            await utils.answer(message, "❌ Галактика не найдена")
            return

        galaxy = self.galaxies[args]
        planets_list = "\n".join([f"• {p}" for p in galaxy["planets"]])
        
        await utils.answer(
            message,
            self.strings["galaxy"].format(
                name=args,
                type=galaxy["type"],
                planets=planets_list
            )
        )

    async def planetcmd(self, message: Message):
        """Информация о планете"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(
                message,
                self.strings["no_args"].format(
                    "\n".join([f"• <code>{p}</code>" for p in self.planets.keys()])
                ) + "\n\nИспользуйте: <code>.planet [название]</code>"
            )
            return

        if args not in self.planets:
            await utils.answer(message, "❌ Планета не найдена")
            return

        planet = self.planets[args]
        await utils.answer(
            message,
            self.strings["planet"].format(
                name=args,
                type=planet["type"],
                mass=planet["mass"],
                diameter=planet["diameter"],
                temp=planet["temp"],
                info=planet["info"]
            )
        )