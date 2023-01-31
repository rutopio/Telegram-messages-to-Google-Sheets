from telethon import TelegramClient, events
from datetime import datetime, timezone, timedelta
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

@client.on(events.NewMessage(chats = channels_name))
async def my_event_handler(event):
    sender = await event.get_sender()
    local_time = event.date.astimezone(timezone(timedelta(hours = my_timezone)))
    time_string = str(datetime.strftime(local_time, "%Y-%m-%d %H:%M:%S"))

    if sender.last_name is not None:
        name = sender.first_name + sender.last_name
    else:
        name = sender.first_name
    
    try:
        textlen = len(event.text)
    except:
        textlen = 0

    print(f"{time_string} {name}({sender.id}) : {event.text}")
    values = [[time_string, name, sender.id, textlen, event.text]]
    sheet_chats.append_table(values=values) 


client.start()
client.run_until_disconnected()
