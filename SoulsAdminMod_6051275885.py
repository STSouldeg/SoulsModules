# meta developer: @Elizar_SoulsTeam
# requires: aiohttp

import asyncio
import logging
import re
import time
from telethon.tl.types import ChatBannedRights, User
from telethon.errors import UserAdminInvalidError
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class SoulsAdminMod(loader.Module):
    """🛡 SoulsAdmin: Мощный инструмент для управления чатами (Fixed for Termux)"""
    
    strings = {
        "name": "SoulsAdmin",
        "not_admin": "❌ <b>Я не админ в этом чате!</b>",
        "args_err": "❌ <b>Неверные аргументы.</b>",
        "user_404": "❌ <b>Пользователь не найден.</b>",
        "banned": "👤 <a href=\"tg://user?id={}\">{}</a> <b>забанен!</b>\n📝 Причина: {}",
        "muted": "👤 <a href=\"tg://user?id={}\">{}</a> <b>замучен на {} мин!</b>\n📝 Причина: {}",
        "kick": "👤 <a href=\"tg://user?id={}\">{}</a> <b>кикнут!</b>",
        "unbanned": "✅ <a href=\"tg://user?id={}\">{}</a> <b>разбанен.</b>",
        "warn": "⚠️ <a href=\"tg://user?id={}\">{}</a> <b>получил варн ({}/3)!</b>\n📝 Причина: {}"
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    async def get_user(self, message):
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if reply: return await self.client.get_entity(reply.sender_id)
        if args:
            try:
                user = args.split()[0]
                if user.isdigit(): user = int(user)
                return await self.client.get_entity(user)
            except: return None
        return None

    @loader.command(ru_doc="[реплай/юзер] [причина] - Забанить")
    async def bancmd(self, message):
        """Забанить пользователя"""
        user = await self.get_user(message)
        if not user: return await utils.answer(message, self.strings["user_404"])
        
        args = utils.get_args_raw(message)
        reason = args.split(maxsplit=1)[1] if args and len(args.split()) > 1 else "Не указана"
        
        try:
            await self.client.edit_permissions(message.chat_id, user.id, view_messages=False)
            await utils.answer(message, self.strings["banned"].format(user.id, user.first_name, reason))
        except:
            await utils.answer(message, self.strings["not_admin"])

    @loader.command(ru_doc="[реплай/юзер] [время в мин] [причина] - Замутить")
    async def mutecmd(self, message):
        """Замутить пользователя"""
        user = await self.get_user(message)
        if not user: return await utils.answer(message, self.strings["user_404"])
        
        args = utils.get_args_raw(message).split()
        t = int(args[1]) if len(args) > 1 and args[1].isdigit() else 0
        reason = " ".join(args[2:]) if len(args) > 2 else "Не указана"
        
        until = time.time() + (t * 60) if t > 0 else None
        
        try:
            await self.client.edit_permissions(message.chat_id, user.id, until_date=until, send_messages=False)
            await utils.answer(message, self.strings["muted"].format(user.id, user.first_name, t if t > 0 else "навсегда", reason))
        except:
            await utils.answer(message, self.strings["not_admin"])

    @loader.command(ru_doc="[реплай/юзер] - Разбанить/Размутить")
    async def unbancmd(self, message):
        """Разбанить/Размутить пользователя"""
        user = await self.get_user(message)
        if not user: return await utils.answer(message, self.strings["user_404"])
        
        try:
            await self.client.edit_permissions(message.chat_id, user.id, view_messages=True, send_messages=True, send_media=True, send_stickers=True, send_gifs=True)
            await utils.answer(message, self.strings["unbanned"].format(user.id, user.first_name))
        except:
            await utils.answer(message, self.strings["not_admin"])

    @loader.command(ru_doc="[реплай/юзер] - Кикнуть")
    async def kickcmd(self, message):
        """Кикнуть пользователя"""
        user = await self.get_user(message)
        if not user: return await utils.answer(message, self.strings["user_404"])
        
        try:
            await self.client.kick_participant(message.chat_id, user.id)
            await utils.answer(message, self.strings["kick"].format(user.id, user.first_name))
        except:
            await utils.answer(message, self.strings["not_admin"])

    @loader.command(ru_doc="Очистить чат от удаленных аккаунтов")
    async def delaccscmd(self, message):
        """Удалить 'собак' из чата"""
        await utils.answer(message, "🔍 <b>Ищу удаленные аккаунты...</b>")
        kicked = 0
        async for user in self.client.iter_participants(message.chat_id):
            if user.deleted:
                try:
                    await self.client.kick_participant(message.chat_id, user.id)
                    kicked += 1
                except: pass
        await utils.answer(message, f"✅ <b>Удалено {kicked} мертвых душ.</b>")