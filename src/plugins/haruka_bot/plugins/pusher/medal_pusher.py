import asyncio
import traceback
from datetime import datetime, timedelta

from nonebot.log import logger
from plugins.haruka_bot.libs.medal import Medal

from ...libs.bilireq import BiliReq
from ...database import DB
from ...libs.medal import Medal
from ...utils import safe_send, scheduler

last_medal = {}

@scheduler.scheduled_job('interval', seconds=10, id='medal_sched')
async def dy_sched():
    """牌子推送"""

    async with DB() as db:
        uid = await db.next_uid('medal')
        if not uid:
            return
        user = await db.get_user(uid)
        assert user is not None
        name = user.name

    logger.debug(f'爬取牌子 {name}（{uid}）')
    br = BiliReq()

    medal = (await br.get_info(uid))['medal']#['medal_name'] # 获取牌子名
    # if uid_info['fans_medal']['show'] == False:
    #     return
    # if uid_info['fans_medal']['wear'] == False:
    #     return
    if medal == None:
        return
    medal = Medal(medal)
    #medal_name = uid_info['fans_medal']['metal']['medal_name']
    # config['uid'][uid]['name'] = dynamics[0]['desc']['user_profile']['info']['uname']
    # await update_config(config)

    # if len(dynamics) == 0: # 没有发过动态或者动态全删的直接结束
    #     return

    if uid not in last_medal: # 没有爬取过这位主播就把最新一条动态时间为 last_time
        #dynamic = Dynamic(dynamics[0])
        last_medal[uid] = medal.medal_name
        return
    
    #for dynamic in dynamics[4::-1]: # 从旧到新取最近5条动态
    #dynamic = Dynamic(dynamic)
    if medal.medal_name != last_medal[uid]:
        logger.info(f"检测到新牌子（{medal.medal_name}）：{name}（{uid}）")
        # image = None
        # for _ in range(3):
        #     try:
        #         image = await get_dynamic_screenshot(dynamic.url)
        #         break
        #     except Exception as e:
        #         logger.error("截图失败，以下为错误日志:")
        #         logger.error(traceback(e))
        #     await asyncio.sleep(0.1)
        # if not image:
        #     logger.error("已达到重试上限，将在下个轮询中重新尝试")
        await medal.format(name)

        async with DB() as db:
            push_list = await db.get_push_list(uid, 'medal')
            for sets in push_list:
                await safe_send(sets.bot_id, sets.type, sets.type_id, medal.message)

        last_medal[uid] = medal.medal_name
    #await DB.update_user(uid, dynamic.name) # type: ignore
