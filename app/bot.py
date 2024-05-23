from telethon import TelegramClient, events
import os
import re
import logging

logging.basicConfig(level=logging.INFO)

api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
bot_token = os.getenv('TELEGRAM_API_TOKEN')

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

async def download_video(event, telegram_url):
    try:
        parts = telegram_url.split('/')
        if len(parts) < 5:
            await event.reply('Provide valid URL.')
            return

        chat_username = parts[3]
        message_id = int(parts[4])

        chat = await client.get_entity(chat_username)
        message = await client.get_messages(chat, ids=message_id)

        if message.video:
            video = message.video
            sender = await message.get_sender()
            sender_name = sender.username if sender.username else sender.first_name

            await client.send_file(event.chat_id, video, caption=f'Video from {telegram_url}')
            logging.info(f'Handled for the URL: {telegram_url}')
        else:
            await event.reply('Has no video.')
    except ValueError:
        await event.reply('Incorrect URL.')
    except Exception as e:
        await event.reply(f'Error: {e}')

@client.on(events.NewMessage(pattern='/download'))
async def handler_download(event):
    if event.is_private:
        message_text = event.message.message

        match = re.search(r'/download (.+)', message_text)
        if match:
            telegram_url = match.group(1)
            await download_video(event, telegram_url)
        else:
            await event.reply('Paste valid URL')

@client.on(events.NewMessage(pattern='/dl'))
async def handler_dl(event):
    if event.is_private:
        message_text = event.message.message

        match = re.search(r'/dl (.+)', message_text)
        if match:
            telegram_url = match.group(1)
            await download_video(event, telegram_url)
        else:
            await event.reply('Paste valid URL')

logging.info("Bot has been launched.")
client.run_until_disconnected()