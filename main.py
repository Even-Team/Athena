import telebot
import wikipedia
import re
from telebot import types
from warnings import filterwarnings
from gtts import gTTS
import os
import tempfile
import hashlib
import requests
from urllib.parse import urljoin

filterwarnings("ignore", category=UserWarning, module='wikipedia')


bot = telebot.TeleBot('7967328415:AAHOjXfv8Oa8ChCTRTuJJ-gBUASpV5EfZHA')

current_language = 'en'

search_results = {}


language_texts = {
    'en': {
        'welcome': "Welcome to Wikipedia Bot! Type any word or topic to search Wikipedia.",
        'language_changed': "Language set to English. Now you can search Wikipedia.",
        'help': "If the bot isn't working, try restarting it. For further assistance, contact: @ETeamev",
        'info': "This bot searches Wikipedia. Just type any word or topic to find information about it.\n"
                "Use /language command to change language.\n"
                "Use /help for assistance.\n\n"
                "Example in runes: {runes_example}",
        'even_team': "EvenTeam creates Telegram bots, games, and more. Check out our Minecraft server: t.me/gigaxserver",
        'options': "Options:",
        'no_content': "Sorry, the content is no longer available.",
        'audio_error': "Sorry, couldn't generate audio.",
        'general_error': "An error occurred.",
        'runic_error': "An error occurred while generating runic text.",
        'no_image': "No image available for this article.",
        'listen_button': "Listen to full text",
        'runes_button': "Show in runes"
    },
    'ru': {
        'welcome': "Добро пожаловать в Wikipedia Bot! Введите любое слово или тему для поиска в Википедии.",
        'language_changed': "Язык изменён на русский. Теперь вы можете искать в Википедии.",
        'help': "Если бот не работает, попробуйте перезапустить его. Для дополнительной помощи обращайтесь: @ETeamev",
        'info': "Этот бот ищет информацию в Википедии. Просто введите любое слово или тему, чтобы найти информацию о ней.\n"
                "Используйте команду /language для изменения языка.\n"
                "Используйте /help для получения помощи.\n\n"
                "Пример в рунах: {runes_example}",
        'even_team': "EvenTeam создает Telegram ботов, игры и многое другое. Посетите наш Minecraft сервер: t.me/gigaxserver",
        'options': "Опции:",
        'no_content': "Извините, содержимое больше недоступно.",
        'audio_error': "Извините, не удалось сгенерировать аудио.",
        'general_error': "Произошла ошибка.",
        'runic_error': "Произошла ошибка при генерации рунического текста.",
        'no_image': "Для этой статьи нет изображения.",
        'listen_button': "Прослушать текст",
        'runes_button': "Показать рунами"
    },
    'de': {
        'welcome': "Willkommen beim Wikipedia Bot! Geben Sie ein beliebiges Wort oder Thema ein, um in Wikipedia zu suchen.",
        'language_changed': "Sprache auf Deutsch geändert. Sie können jetzt Wikipedia durchsuchen.",
        'help': "Wenn der Bot nicht funktioniert, versuchen Sie ihn neu zu starten. Für weitere Hilfe kontaktieren Sie: @ETeamev",
        'info': "Dieser Bot durchsucht Wikipedia. Geben Sie einfach ein beliebiges Wort oder Thema ein, um Informationen darüber zu finden.\n"
                "Verwenden Sie den Befehl /language, um die Sprache zu ändern.\n"
                "Verwenden Sie /help für Hilfe.\n\n"
                "Beispiel in Runen: {runes_example}",
        'even_team': "EvenTeam erstellt Telegram Bots, Spiele und mehr. Besuchen Sie unseren Minecraft Server: t.me/gigaxserver",
        'options': "Optionen:",
        'no_content': "Entschuldigung, der Inhalt ist nicht mehr verfügbar.",
        'audio_error': "Entschuldigung, Audio konnte nicht generiert werden.",
        'general_error': "Ein Fehler ist aufgetreten.",
        'runic_error': "Bei der Generierung der Runenschrift ist ein Fehler aufgetreten.",
        'no_image': "Kein Bild für diesen Artikel verfügbar.",
        'listen_button': "Text anhören",
        'runes_button': "In Runen anzeigen"
    },
    'fo': {
        'welcome': "Vælkomin til Wikipedia Bot! Skriva eitt orð ella evni fyri at leita í Wikipedia.",
        'language_changed': "Mál stilla á føroyskt. Nú kanst tú leita í Wikipedia.",
        'help': "Um bótin virkar ikki, royn at endurbyrja hana. Fyri meiri hjálp, kontakt: @ETeamev",
        'info': "Henda bótan leitar í Wikipedia. Skriva bara eitt orð ella evni fyri at finna upplýsingar um tað.\n"
                "Nýt /language fyri at broyta mál.\n"
                "Nýt /help fyri hjálp.\n\n"
                "Dømi í rún: {runes_example}",
        'even_team': "EvenTeam gerir Telegram bótir, leikir og meira. Kík á okkara Minecraft ambæt: t.me/gigaxserver",
        'options': "Møguleikar:",
        'no_content': "Tíverri, innihaldið er ikki longur tøkt.",
        'audio_error': "Tíverri, kundi ikki gera ljóð.",
        'general_error': "Ein feilur hendi.",
        'runic_error': "Ein feilur hendi meðan rún vórðu gjørdar.",
        'no_image': "Ongin mynd er tøk til hesa grein.",
        'listen_button': "Hoyra tekstin",
        'runes_button': "Vís við rún"
    },
    'non': {
        'welcome': "Velkomin til Wikipedia-bóta! Skrifaðu hvaða orð eða efni til að leita í Wikipedia.",
        'language_changed': "Tungu breytt í norrænu. Nú getur þú leitað í Wikipedia.",
        'help': "Ef bótan virkar ekki, reyndu að endurræsa hana. Fyrir frekari aðstoð, hafðu samband við: @ETeamev",
        'info': "Þessi bóta leitar í Wikipedia. Skrifaðu bara hvaða orð eða efni til að finna upplýsingar um það.\n"
                "Notaðu /language til að breyta tungumáli.\n"
                "Notaðu /help fyrir aðstoð.\n\n"
                "Dæmi í rúnum: {runes_example}",
        'even_team': "EvenTeam býr til Telegram-bóta, leiki og fleira. Skoðaðu Minecraft-þjóninn okkar: t.me/gigaxserver",
        'options': "Valkostir:",
        'no_content': "Því miður, efnið er ekki lengur tiltækt.",
        'audio_error': "Því miður, gat ekki búið til hljóð.",
        'general_error': "Villa kom upp.",
        'runic_error': "Villa kom upp við að búa til rúnatexta.",
        'no_image': "Engin mynd fyrir þessa grein.",
        'listen_button': "Hlusta á texta",
        'runes_button': "Sýna með rúnum"
    }
}


def get_wiki_page(search_term):
    try:
        wiki_lang = 'en' if current_language == 'non' else current_language
        wikipedia.set_lang(wiki_lang)

        page = wikipedia.page(search_term, auto_suggest=False)
        return page
    except Exception as e:
        print(f"Error getting wiki page: {e}")
        return None


def get_wiki_content(page):
    try:
        content = page.content[:1500]
        sentences = content.split('.')[:-1]

        clean_text = '.'.join(
            sentence.strip() + '.'
            for sentence in sentences
            if len(sentence.strip()) > 3 and not ('==' in sentence)
        )

        clean_text = re.sub(r'\([^()]*\)', '', clean_text)  # Remove parentheses
        clean_text = re.sub(r'\{[^{}]*\}', '', clean_text)  # Remove curly braces
        return clean_text if clean_text else language_texts[current_language].get('no_content',
                                                                                  "No readable content found.")
    except Exception as e:
        print(f"Error processing content: {e}")
        return language_texts[current_language].get('no_content', "No content available.")


def get_wiki_image_url(page):
    try:
        if not hasattr(page, 'images') or not page.images:
            return None

        # Get the first image that's not a flag or icon
        for img_url in page.images:
            if img_url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                if 'flag' not in img_url.lower() and 'icon' not in img_url.lower():
                    return img_url
        return page.images[0] if page.images else None
    except Exception as e:
        print(f"Error getting image URL: {e}")
        return None


def download_image(image_url):
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
                return f.name
        return None
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None


def getwiki(search_term):
    try:
        page = get_wiki_page(search_term)
        if not page:
            return language_texts[current_language].get('no_content', "No Wikipedia page found for this term."), None

        content = get_wiki_content(page)
        image_url = get_wiki_image_url(page)

        return content, image_url
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple options found. Please be more specific. Options: {', '.join(e.options[:5])}...", None
    except Exception as e:
        return f"An error occurred: {str(e)}", None


def to_runes(text):
    rune_map = {
        'a': 'ᛅ', 'á': 'ᛅ', 'b': 'ᛒ', 'c': 'ᛋ', 'd': 'ᛏ', 'ð': 'ᚦ', 'e': 'ᛁ',
        'é': 'ᛁ', 'f': 'ᚠ', 'g': 'ᚴ', 'h': 'ᚼ', 'i': 'ᛁ', 'í': 'ᛁ', 'j': 'ᛁ',
        'k': 'ᚴ', 'l': 'ᛚ', 'm': 'ᛘ', 'n': 'ᚾ', 'o': 'ᚢ', 'ó': 'ᚢ', 'ǫ': 'ᚢ',
        'p': 'ᛒ', 'q': 'ᚴ', 'r': 'ᚱ', 's': 'ᛋ', 't': 'ᛏ', 'u': 'ᚢ', 'ú': 'ᚢ',
        'v': 'ᚠ', 'w': 'ᚠ', 'x': 'ᛋ', 'y': 'ᚢ', 'ý': 'ᚢ', 'z': 'ᛋ', 'æ': 'ᛅ',
        'ø': 'ᚢ', 'ö': 'ᚢ', 'þ': 'ᚦ', ' ': ' ', '.': '·', ',': '·', ':': '·',
        '!': '·', '?': '·'
    }

    runic_text = []
    for char in text.lower():
        if char in rune_map:
            runic_text.append(rune_map[char])
        else:
            runic_text.append(char)

    return ''.join(runic_text)


def text_to_speech(text, lang):
    try:
        tts_lang = 'is' if lang == 'non' else lang

        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            temp_path = fp.name

        tts = gTTS(text=text[:5000], lang=tts_lang)
        tts.save(temp_path)
        return temp_path
    except Exception as e:
        print(f"Error in TTS: {e}")
        return None


def get_language_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("English"))
    markup.add(types.KeyboardButton("Русский"))
    markup.add(types.KeyboardButton("Deutsch"))
    markup.add(types.KeyboardButton("Føroyskt"))
    markup.add(types.KeyboardButton("Norrǿna"))
    return markup


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,
                     language_texts[current_language]['welcome'],
                     reply_markup=get_language_keyboard())


@bot.message_handler(commands=["language"])
def change_language(message):
    bot.send_message(message.chat.id, 'Please choose your language:',
                     reply_markup=get_language_keyboard())

@bot.message_handler(commands=["commands"])
def say_commands(message):
    bot.send_message(message.chat.id, '/help, /info,/text, /EvenTeam')

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id,
                     language_texts[current_language]['help'],
                     reply_markup=get_language_keyboard())


@bot.message_handler(commands=["info"])
def info(message):
    example_runes = to_runes("example in old norse")
    bot.send_message(message.chat.id,
                     language_texts[current_language]['info'].format(runes_example=example_runes),
                     reply_markup=get_language_keyboard())


@bot.message_handler(commands=["EvenTeam"])
def even_team(message):
    bot.send_message(message.chat.id,
                     language_texts[current_language]['even_team'],
                     reply_markup=get_language_keyboard())


@bot.message_handler(content_types=["text"])
def handle_text(message):
    global current_language, search_results
    text = message.text.strip()

    lang_map = {
        'Русский': 'ru',
        'English': 'en',
        'Deutsch': 'de',
        'Føroyskt': 'fo',
        'Norrǿna': 'non'
    }

    if text in lang_map:
        current_language = lang_map[text]
        response = language_texts[current_language]['language_changed']
        bot.send_message(message.chat.id, response,
                         reply_markup=get_language_keyboard())
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        result, image_url = getwiki(text)

        search_id = hashlib.md5(result.encode()).hexdigest()[:10]
        search_results[search_id] = {'text': result, 'image_url': image_url}


        if image_url:
            try:
                image_path = download_image(image_url)
                if image_path:
                    with open(image_path, 'rb') as photo:
                        bot.send_photo(message.chat.id, photo)
                    os.unlink(image_path)
                else:
                    bot.send_message(message.chat.id, language_texts[current_language]['no_image'])
            except Exception as e:
                print(f"Error sending image: {e}")
                bot.send_message(message.chat.id, language_texts[current_language]['no_image'])


        bot.send_message(message.chat.id, result,
                         reply_markup=get_language_keyboard())


        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            "🔊 " + language_texts[current_language]['listen_button'],
            callback_data=f"speak:{search_id}"
        ))

        if current_language == 'non':
            markup.add(types.InlineKeyboardButton(
                "🔣 " + language_texts[current_language]['runes_button'],
                callback_data=f"runes:{search_id}"
            ))

        bot.send_message(message.chat.id, language_texts[current_language]['options'],
                         reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('speak:'))
def speak_callback(call):
    try:
        search_id = call.data[6:]
        if search_id not in search_results:
            bot.answer_callback_query(call.id, language_texts[current_language]['no_content'])
            return

        text_to_speak = search_results[search_id]['text']
        tts_lang_map = {
            'en': 'en',
            'ru': 'ru',
            'de': 'de',
            'fo': 'da',
            'non': 'is'
        }

        tts_lang = tts_lang_map.get(current_language, 'en')
        bot.send_chat_action(call.message.chat.id, 'record_audio')
        audio_path = text_to_speech(text_to_speak, tts_lang)

        if audio_path:
            with open(audio_path, 'rb') as audio:
                bot.send_voice(call.message.chat.id, audio,
                               reply_markup=get_language_keyboard())
            os.unlink(audio_path)
        else:
            bot.answer_callback_query(call.id, language_texts[current_language]['audio_error'])

    except Exception as e:
        print(f"Error in callback: {e}")
        bot.answer_callback_query(call.id, language_texts[current_language]['general_error'])


@bot.callback_query_handler(func=lambda call: call.data.startswith('runes:'))
def runes_callback(call):
    try:
        search_id = call.data[6:]
        if search_id not in search_results:
            bot.answer_callback_query(call.id, language_texts[current_language]['no_content'])
            return

        original_text = search_results[search_id]['text']
        runic_text = to_runes(original_text)
        runic_text = runic_text[:4000] + "..." if len(runic_text) > 4000 else runic_text

        bot.send_message(call.message.chat.id, f"Runic version:\n\n{runic_text}")
        bot.answer_callback_query(call.id)

    except Exception as e:
        print(f"Error in runes callback: {e}")
        bot.answer_callback_query(call.id, language_texts[current_language]['runic_error'])


if __name__ == '__main__':
    print("Bot is running...")
    bot.polling(none_stop=True)