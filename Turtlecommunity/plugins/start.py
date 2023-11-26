import time
import glob

from importlib import import_module

from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from Turtlecommunity.utils import tld, add_lang


HELPABLE: list[str] = []

for modules in glob.glob("Turtlecommunity/plugins/*.py"):
    imported_module = import_module((modules)[:-3].replace("/", "."))
    if hasattr(imported_module, "__help__"):
        HELPABLE.append((modules.replace("/", ".")).split(".")[-2])


@Client.on_callback_query(filters.regex(pattern=r"^start_back$"))
@Client.on_message(filters.command("start"))
async def start(c: Client, m: Message | CallbackQuery):
    chat = m.chat if isinstance(m, Message) else m.message.chat
    msg = (await tld(chat.id, "<i>Olá <b>{}</b>!! Meu nome é <b>{}</b>. Estou aqui para divertir seu grupo</i>, <b>Fui feito com a biblioteca Pyrogram</b>")).format(m.from_user.mention, c.me.first_name)
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboadButton(
                    text=await tld(chat.id, "🌐 Idioma"), callback_data="lang_menu"),
            ],
            [
                InlineKeyboardButton(
                    text=await tld(chat.id, "ℹ️ Sobre"), callback_data="about"),
                InlineKeyboardButton(
                    text=await tld(chat.id, "📚 Comandos"), callback_data="help_menu"),
            ],
        ]
    )
    if isinstance(m, Message):
        await m.reply(text=msg, reply_markup=button)
    else:
        await c.edit_message_text(
            chat_id=m.message.chat.id,
            message_id=m.message.id,
            text=msg,
            reply_markup=button,
        )

@Client.on_callback_query(filters.regex(pattern=r"about"))
async def about_menu(c: Client, cb: CallbackQuery):
    keyboard = [
        [
            InlineKeyboardButton("⬅️ Voltar", "start_back"),
        ],
    ]
    text = ("<b>— yDixx</b>\n<b>Versão: <i>{}</i>").format("1.0.1")
    await cb.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True)

@WhiterX.on_callback_query(filters.regex(pattern=r"^lang_menu$"))
async def infos(client: WhiterX, cb: CallbackQuery):
    info_text = await tld(cb.message.chat.id, "Escolha seu idioma:")
    language_flag = "🇧🇷 Português" if lang == "pt" else "🇺🇸 English" if lang == "en" else "🇪🇸 Espanõl"
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🇺🇸 English", callback_data=f"lang.en"),
                InlineKeyboardButton("🇧🇷 Português", callback_data=f"lang.pt"),
                InlineKeyboardButton("🇪🇸 Español", callback_data=f"lang.es"),
            ],
            [
                InlineKeyboardButton(await tld(cb.message.chat.id, "⬅️ Voltar"), callback_data="start_back"),
            ]
        ]
    )
    await client.edit_message_text(
        chat_id=cb.message.chat.id,
        message_id=cb.message.id,
        text=info_text,
        reply_markup=button,
    )

@WhiterX.on_callback_query(filters.regex(pattern="^lang\.(.+?)"))
async def infos(c: WhiterX, cb: CallbackQuery):
    try:
        lang = cb.data.split(".")[1]
    except ValueError:
        return print(cb.data)
    language_flag = "🇧🇷 Português" if lang == "pt" else "🇺🇸 English" if lang == "en" else "🇪🇸 Espanõl"
    await add_lang(cb.message.chat.id, lang)
    time.sleep(0.5)
    info_text = await tld(cb.message.chat.id, "<i>O idioma foi alterado com sucesso para {}")
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(await tld(cb.message.chat.id, "⬅️ Voltar"), callback_data="start_back"),
            ]
        ]
    )
    await c.edit_message_text(
        chat_id=cb.message.chat.id,
        message_id=cb.message.id,
        text=info_text.format(language_flag),
        reply_markup=button,
    )
