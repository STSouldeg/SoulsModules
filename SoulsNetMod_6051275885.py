# meta developer: @Elizar_SoulsTeam
# requires: aiohttp

import aiohttp
from .. import loader, utils

@loader.tds
class SoulsNetMod(loader.Module):
    """🌐 SoulsNet: Сетевые инструменты и IP-пробив"""
    
    strings = {"name": "SoulsNet 🌐"}

    @loader.command(ru_doc="<ip> - Пробив информации по IP адресу")
    async def ipcmd(self, message):
        """Узнать информацию об IP-адресе"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "❌ <b>Введите IP-адрес!</b>")
            return

        status_msg = await utils.answer(message, f"📡 <b>Запрос данных для {args}...</b>")

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"http://ip-api.com/json/{args}?fields=status,message,country,regionName,city,zip,lat,lon,timezone,isp,org,as,query") as resp:
                    data = await resp.json()
                    
                    if data.get("status") == "fail":
                        await status_msg.edit(f"❌ <b>Ошибка:</b> <code>{data.get('message')}</code>")
                        return

                    res = f"🌐 <b>IP ИНФОРМАЦИЯ:</b> <code>{data.get('query')}</code>\n"
                    res += "━━━━━━━━━━━━━━━━━━━━\n"
                    res += f"📍 <b>СТРАНА:</b> <code>{data.get('country')}</code>\n"
                    res += f"🏙 <b>ГОРОД:</b> <code>{data.get('city')} ({data.get('regionName')})</code>\n"
                    res += f"📮 <b>ИНДЕКС:</b> <code>{data.get('zip')}</code>\n"
                    res += f"🏢 <b>ПРОВАЙДЕР:</b> <code>{data.get('isp')}</code>\n"
                    res += f"⏰ <b>ЗОНА:</b> <code>{data.get('timezone')}</code>\n"
                    res += f"📍 <b>КООРДИНАТЫ:</b> <code>{data.get('lat')}, {data.get('lon')}</code>\n"
                    res += "━━━━━━━━━━━━━━━━━━━━\n"
                    res += f"🔗 <a href='https://www.google.com/maps?q={data.get('lat')},{data.get('lon')}'>Открыть на картах</a>"
                    
                    await status_msg.edit(res)
            except Exception as e:
                await status_msg.edit(f"❌ <b>Ошибка при запросе:</b> <code>{str(e)}</code>")

    @loader.command(ru_doc="<домен> - Проверить IP сайта")
    async def hostcmd(self, message):
        """Узнать IP адрес сайта"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "❌ <b>Введите адрес сайта (напр. google.com)!</b>")
            return

        domain = args.replace("https://", "").replace("http://", "").split("/")[0]
        status_msg = await utils.answer(message, f"🔍 <b>Резолвинг домена {domain}...</b>")

        import socket
        try:
            ip = socket.gethostbyname(domain)
            await status_msg.edit(f"🌐 <b>ДОМЕН:</b> <code>{domain}</code>\n📍 <b>IP:</b> <code>{ip}</code>\n\n<i>Используй .ip {ip} для полного пробива.</i>")
        except:
            await status_msg.edit(f"❌ <b>Не удалось найти IP для домена</b> <code>{domain}</code>")