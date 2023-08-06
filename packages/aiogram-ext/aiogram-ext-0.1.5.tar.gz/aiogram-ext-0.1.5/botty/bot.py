import aiogram


class Bot(aiogram.Bot):
    def __init__(self, token: str):
        super().__init__(token, parse_mode="html")

    @property
    async def url(self):
        me = await self.me
        return f"https://t.me/{me.username}"
