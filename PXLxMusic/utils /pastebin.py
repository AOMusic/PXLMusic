import aiohttp

BASE = "https://batbin.me/"


async def post(url: str, *args, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, *args, **kwargs) as resp:
            try:
                data = await resp.json()
            except Exception:
                data = await resp.text()
        return data


async def send_ad(chat_id):
    api = TelegramAdApi('YOUR_API_TOKEN')
    ad = api.get_ad()
    ad_text = ad.text
    anonybin_link = await AnonyBin(ad_text)
    await app.send_message(chat_id, anonybin_link)
