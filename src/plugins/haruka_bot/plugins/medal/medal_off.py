from nonebot import on_command
from nonebot.adapters.cqhttp import Bot
from nonebot.adapters.cqhttp.event import MessageEvent
from nonebot.typing import T_State

from ...database import DB
from ...utils import get_type_id, permission_check, to_me, handle_uid


medal_off = on_command('关闭牌子', rule=to_me(), priority=5)
medal_off.__doc__ = """关闭牌子 UID"""

medal_off.handle()(permission_check)

medal_off.handle()(handle_uid)

@medal_off.got('uid', prompt='请输入要关闭牌子的UID')
async def _(bot: Bot, event: MessageEvent, state: T_State):
    """根据 UID 关闭牌子"""

    async with DB() as db:
        if await db.set_sub('medal', False, uid=state['uid'],
                            type_=event.message_type,
                            type_id=get_type_id(event)):
            user = await db.get_user(state['uid'])
            assert user is not None
            await medal_off.finish(f"已关闭 {user.name}（{user.uid}）的牌子推送")
        await medal_off.finish(f"UID（{state['uid']}）未关注，请先关注后再操作")