# meta developer: @Elizar_SoulsTeam
from .. import loader, utils

@loader.tds
class EmergencyFixMod(loader.Module):
    """Скрипт экстренной очистки базы данных."""
    strings = {"name": "EmergencyFix"}

    @loader.command()
    async def clean_soul(self, message):
        """Полная очистка конфигов SoulOmnipotence"""
        self.db.set("SoulOmnipotence", "shackle", None)
        self.db.set("SoulOmnipotence", "ghost", False)
        self.db.set("SoulOmnipotence", "anti", False)
        self.db.set("SoulOmnipotence", "zcall", False)
        await utils.answer(message, "<b>✅ База данных SoulOmnipotence полностью очищена. Цепи сняты.</b>")