from nonebot.adapters.cqhttp.message import MessageSegment


class Medal():
    def __init__(self, medal):
        # self.origin = json.loads(self.card['origin'])
        self.medal = medal
        # self.card = json.loads(dynamic['card'])
        # self.dynamic['card'] = self.card
        self.target_id = medal['target_id']
        self.medal_name = medal['medal_name']
        self.url = "https://t.bilibili.com/" + str(self.target_id)
        #self.time = dynamic['desc']['timestamp']
        # self.origin_id = dynamic['desc']['orig_dy_id']
        self.uid = medal['uid']
        #self.name = dynamic['desc']['user_profile']['info'].get('uname')
        # self.name = dynamic['desc']['user_profile']['info'].get('uname', Config.get_name(self.uid))

    async def format(self,uname):
        # type_msg = {
        #     0: "换了新牌子"
        #     # 1: "转发了一条动态",
        #     # 8: "发布了新投稿",
        #     # 16: "发布了短视频",
        #     # 64: "发布了新专栏",
        #     # 256: "发布了新音频"
        # }
        self.message = (f"{uname} " +
                        f"换了新牌子："+self.medal_name+"\n" +
                        f"{self.url}\n"
                        #MessageSegment.image(f"base64://{img}")
                        )
