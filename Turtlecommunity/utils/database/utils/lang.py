import json
import yaml
import logging
import pathlib

from gpytranslate import Translator

CHAT_LANG = "Turtlecommunity/utils/database/chat_language.json
STRINGS = "locales/base.yml"

tr = Translator()

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

async def tld(gid: int, string) -> str:
    lang_ = await get_chat_lang(gid)
    text = language_string.get("base").get(string)
    tr_ = await tr.translate(text, targetlang=lang_)
    return tr_

def get_all_files():
    path = pathlib.Path(STRINGS)
    return [i.absolute() for i in path.glob("**/*")]

def load_language():
    all_files = get_all_files()
    for filepath in all_files:
        with open(filepath) as f:
            data = yaml.safe_load(f)
            language_to_load = data.get("language")
            language_string[language_to_load] = data
    logging.info("All language Loaded.")
