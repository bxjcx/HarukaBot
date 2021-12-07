from nonebot import on_command
from nonebot.adapters.cqhttp import Bot
from nonebot.adapters.cqhttp.event import MessageEvent
from nonebot.typing import T_State

from ...database import DB
from ...utils import get_type_id, permission_check, to_me, handle_uid


medal_on = on_command('开启牌子', rule=to_me(), priority=5)
medal_on.__doc__ = """开启牌子 UID"""

medal_on.handle()(permission_check)

medal_on.handle()(handle_uid)

@medal_on.got('uid', prompt='请输入要开启牌子的UID')
async def _(bot: Bot, event: MessageEvent, state: T_State):
    """根据 UID 开启牌子"""

    async with DB() as db:
        if await db.set_sub('medal', True, uid=state['uid'],
                            type_=event.message_type,
                            type_id=get_type_id(event)):
            user = await db.get_user(state['uid'])
            assert user is not None
            await medal_on.finish(f"已开启 {user.name}（{user.uid}）的牌子推送")
        await medal_on.finish(f"UID（{state['uid']}）未关注，请先关注后再操作")