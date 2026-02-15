# meta developer: @Elizar_SoulsTeam

from .. import loader, utils

@loader.tds
class SoulReleaseMod(loader.Module):
    """Экстренное снятие всех ограничений и цепей."""
    strings = {"name": "SoulRelease"}

    @loader.command()
    async def stopall(self, message):
        """Разорвать все цепи и сбросить настройки SoulOmnipotence"""
        self.db.set("SoulOmnipotence", "shackle", None)
        self.db.set("SoulOmnipotence", "ghost", False)
        self.db.set("SoulOmnipotence", "pulse", False)
        self.db.set("SoulOmnipotence", "anti", False)
        
        # Попытка найти активный модуль в памяти и сбросить его переменные напрямую
        for mod in self.all_modules:
            if mod.strings.get("name") == "SoulOmnipotence":
                mod.shackle_target = None
                mod.ghost = False
                mod.aura_active = False
        
        await utils.answer(message, "<b>⛓ ЦЕПИ РАЗОРВАНЫ. Все системы SoulOmnipotence переведены в режим ожидания.</b>")