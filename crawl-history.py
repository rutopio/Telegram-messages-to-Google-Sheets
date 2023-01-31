from telethon import TelegramClient, events
from datetime import datetime,timezone,timedelta
import pygsheets
import pandas as pd

# Telegram Settings: https://my.telegram.org/ 
api_id = INT_TELEGRAM_API_ID
api_hash = 'STR_TELEGRAM_API_HASH'

# Both works
channels_name = "STR_CHANNEL_INVITE_LINK"
channels_name = INT_TELEGRAM_CHANNEL_OR_GROUP_ID

# Google Sheets Settings
auth_file = "credentials.json"
sheet_url = "STR_GOOGLE_SHEETS_LINK" 
gc = pygsheets.authorize(service_file = auth_file)
sheet = gc.open_by_url(sheet_url)
sheet_chats = sheet.worksheet_by_title("STR_SHEET_NAME")

# Time Zone
my_timezone = +8

client = TelegramClient('session', api_id, api_hash)

async def main():
    values = []

    async for message in client.iter_messages(target_group, reverse=True):
        sender = await message.get_sender()
        local_time = message.date.astimezone(timezone(timedelta(hours=my_timezone)))
        time_string = str(datetime.strftime(local_time, "%Y-%m-%d %H:%M:%S"))

        if sender.last_name is not None:
            name = sender.first_name + sender.last_name
        else:
            name = sender.first_name
        
        try:
            textlen = len(message.text)
        except:
            textlen = 0

        values.append([time_string, name, sender.id, textlen, message.text])
        print(f"{time_string} {name}({sender.id}) : {message.text}")

    sheet_chats.append_table(values=values)

with client:
    client.loop.run_until_complete(main())
