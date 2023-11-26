import json
import yaml
import logging
import pathlib

from gpytranslate import Translator

CHAT = "Turtlecommunity/utils/database/chat_language.json"

tr = Translator()

language_string = {}

# Função para procurar o objeto com o chat_id dado na lista
def find_lang(chat_id, chat_list):
    for obj in chat_list:
        if obj["chat_id"] == chat_id:
            return obj
    return None

async def add_lang(gid: int, lang: str):
    # Carregar os dados do arquivo JSON
    with open(CHAT, "r") as file:
        chat_lang = json.load(file)
    # Procurar o objeto com o chat_id dado
    obj = find_lang(str(gid), chat_lang)
    # Se o objeto existir, atualizar o lang
    if obj:
        obj["lang"] = lang
    # Se o objeto não existir, criar um novo e adicionar na lista
    else:
        obj = {"chat_id": str(gid), "lang": lang}
        chat_lang.append(obj)
    # Salvar os dados no arquivo JSON
    with open(CHAT, "w") as file:
        json.dump(chat_lang, file)

async def get_chat_lang(gid: int) -> str:
    # Carregar os dados do arquivo JSON
    with open(CHAT, "r") as file:
        chat_lang = json.load(file)
    # Procurar o objeto com o chat_id dado
    obj = find_lang(str(gid), chat_lang)
    # Se o objeto existir, retornar o lang
    if obj:
        return obj.get("lang")
    # Se o objeto não existir, retornar "en"
    else:
        return "en"

async def tld(gid: int, text) -> str:
    lang_ = await get_chat_lang(gid)
    tr_ = await tr.translate(text, targetlang=lang_)
    return tr_
