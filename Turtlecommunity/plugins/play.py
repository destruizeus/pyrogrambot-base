from pyrogram import Client, filters, types
import requests
from io import BytesIO
import urllib.parse

@Client.on_message(filters.command(["play", "mp3"], prefixes=["?", "/"]))
def play(client, message):
    if len(message.command) == 1:
        message.reply_text('vou baixar oq cara?')
        return

    query = " ".join(message.command[1:])
    api_url = f'http://mdzapi.mdzhost.cloud/youtube/play?query={query}&apitoken=zeus7676'

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        result = response.json()

        if 'status' in result and result['status']:
            thumbnail_url = result['Thumb']
            title = result['Title']
            description = result['Description']
            duration = result['Duration']
            views = result['Viewer']
            channel = result['Channel']
            video_link = result['Link']

            message_text = f"🖥 <b>Título:</b> `{title}`\n" \
                           f"📚 <b>Canal:</b> `{channel}`\n"

            reply_markup = types.InlineKeyboardMarkup([
                [types.InlineKeyboardButton("📊 ver no youtube", url=video_link)]
            ])

            download_url = f'http://mdzapi.mdzhost.cloud/youtube/mp3?url={urllib.parse.quote(video_link)}&apitoken=zeus7676'

            audio_response = requests.get(download_url)
            audio_response.raise_for_status()
            audio_file = BytesIO(audio_response.content)
            audio_file.name = f"{title}.mp3"
            message.reply_audio(audio=audio_file, caption=message_text, reply_markup=reply_markup)

        else:
            message.reply_text('sla deu erro')

    except requests.RequestException as e:
        message.reply_text('afe deu erro')
