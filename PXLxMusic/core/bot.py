from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode
import random

import config
from ..logging import LOGGER


class Anony(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot...")
        super().__init__(
            name="AnonXMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=7,
        )
        
        # List of Ads (you can customize these ads)
        self.ads = [
            "🎧 **Check out our sponsor**: [Music Pro] - Best music streaming service! 🎶",
            "🎧 **Try MusicMax**: Unlimited songs, no ads, anytime, anywhere! 🎶",
            "🎧 **Promo**: Get 50% off on your first month with [Music Premium]! 🎵",
        ]

    def show_ad(self):
        """Function to get a random ad from the list."""
        return random.choice(self.ads)

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        try:
            # Send the bot start message to a log group/channel
            ad_text = self.show_ad()  # Get a random ad
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b><u>\n\nɪᴅ : <code>{self.id}</code>\nɴᴀᴍᴇ : {self.name}\nᴜsᴇʀɴᴀᴍᴇ : @{self.username}\n\n{ad_text}",
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "Bot has failed to access the log group/channel. Make sure that you have added your bot to your log group/channel."
            )
            exit()
        except Exception as ex:
            LOGGER(__name__).error(
                f"Bot has failed to access the log group/channel.\n  Reason : {type(ex).__name__}."
            )
            exit()

        a = await self.get_chat_member(config.LOGGER_ID, self.id)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error(
                "Please promote your bot as an admin in your log group/channel."
            )
            exit()
        LOGGER(__name__).info(f"Music Bot Started as {self.name}")

    async def stop(self):
        await super().stop()

    async def send_ad_message(self, chat_id):
        """Method to send an ad message to a specific chat."""
        ad_text = self.show_ad()
        await self.send_message(chat_id, ad_text)
