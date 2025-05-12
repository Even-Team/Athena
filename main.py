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
sound_mode = {}  # Словарь для отслеживания пользователей в режиме sound
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
        'runes_button': "Show in runes",
        'sound_mode_enter': "Sound mode activated. Send me any text and I'll convert it to speech. Type /exit to quit.",
        'sound_mode_exit': "Exited sound mode.",
        'sound_mode_error': "Error generating speech. Please try again."
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
        'runes_button': "Показать рунами",
        'sound_mode_enter': "Режим озвучивания активирован. Отправьте мне любой текст, и я преобразую его в речь. Напишите /exit для выхода.",
        'sound_mode_exit': "Вы вышли из режима озвучивания.",
        'sound_mode_error': "Ошибка генерации речи. Пожалуйста, попробуйте снова."
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
        'runes_button': "In Runen anzeigen",
        'sound_mode_enter': "Sprachmodus aktiviert. Senden Sie mir einen Text und ich werde ihn in Sprache umwandeln. Geben Sie /exit ein, um zu beenden.",
        'sound_mode_exit': "Sprachmodus beendet.",
        'sound_mode_error': "Fehler bei der Sprachgenerierung. Bitte versuchen Sie es erneut."
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
        'runes_button': "Vís við rún",
        'sound_mode_enter': "Ljóðtilfar virknað. Send mær ein tekst, og eg gera hann til ljóð. Skriva /exit fyri at hætta.",
        'sound_mode_exit': "Ljóðtilfar er hætt.",
        'sound_mode_error': "Feilur við at gera ljóð. Royn aftur."
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
        'runes_button': "Sýna með rúnum",
        'sound_mode_enter': "Hljóðhamur virkur. Sendu mér texta og ég breyti honum í hljóð. Skrifaðu /exit til að hætta.",
        'sound_mode_exit': "Hætt í hljóðham.",
        'sound_mode_error': "Villa við að búa til hljóð. Reyndu aftur."
    }
}


def get_language_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('English')
    btn2 = types.KeyboardButton('Русский')
    btn3 = types.KeyboardButton('Deutsch')
    btn4 = types.KeyboardButton('Føroyskt')
    btn5 = types.KeyboardButton('Norrǿna')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    return markup


def getwiki(search_term):
    try:
        wikipedia.set_lang(current_language)
        page = wikipedia.page(search_term)
        summary = wikipedia.summary(search_term, sentences=3)

        # Clean up the summary text
        summary = re.sub(r'\([^)]*\)', '', summary)  # Remove text in parentheses
        summary = re.sub(r'\[[^\]]*\]', '', summary)  # Remove text in brackets
        summary = re.sub(r'\s+', ' ', summary).strip()  # Remove extra whitespace

        # Get image URL if available
        image_url = None
        if page.images:
            for img in page.images:
                if img.lower().endswith(('.jpg', '.jpeg', '.png')):
                    image_url = img
                    break

        return f"{summary}\n\nRead more: {page.url}", image_url
    except wikipedia.exceptions.DisambiguationError as e:
        options = "\n".join(e.options[:5])
        return f"Multiple options found. Please be more specific:\n\n{options}", None
    except wikipedia.exceptions.PageError:
        return f"Sorry, no information found for '{search_term}' in {current_language} Wikipedia.", None
    except Exception as e:
        print(f"Error in getwiki: {e}")
        return "An error occurred while searching Wikipedia.", None


def text_to_speech(text, lang):
    try:
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as fp:
            tts = gTTS(text=text, lang=lang)
            tts.save(fp.name)
            return fp.name
    except Exception as e:
        print(f"Error in text_to_speech: {e}")
        return None


def download_image(url):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as fp:
                for chunk in response.iter_content(1024):
                    fp.write(chunk)
                return fp.name
    except Exception as e:
        print(f"Error downloading image: {e}")
    return None


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,
                     language_texts[current_language]['welcome'],
                     reply_markup=get_language_keyboard())


@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id,
                     language_texts[current_language]['help'],
                     reply_markup=get_language_keyboard())


@bot.message_handler(commands=["info"])
def info(message):
    runes_example = "ᚺᛖᛚᛚᛟ ᚹᛟᚱᛚᛞ"  # Example runic text
    text = language_texts[current_language]['info'].format(runes_example=runes_example)
    bot.send_message(message.chat.id,
                     text,
                     reply_markup=get_language_keyboard())


@bot.message_handler(commands=["even_team"])
def even_team(message):
    bot.send_message(message.chat.id,
                     language_texts[current_language]['even_team'],
                     reply_markup=get_language_keyboard())


@bot.message_handler(commands=["language"])
def language(message):
    bot.send_message(message.chat.id,
                     "Choose language:",
                     reply_markup=get_language_keyboard())


@bot.message_handler(commands=["sound"])
def enter_sound_mode(message):
    user_id = message.from_user.id
    sound_mode[user_id] = True
    bot.send_message(message.chat.id,
                     language_texts[current_language]['sound_mode_enter'],
                     reply_markup=get_language_keyboard())


@bot.message_handler(commands=["exit"])
def exit_sound_mode(message):
    user_id = message.from_user.id
    if user_id in sound_mode:
        del sound_mode[user_id]
    bot.send_message(message.chat.id,
                     language_texts[current_language]['sound_mode_exit'],
                     reply_markup=get_language_keyboard())


@bot.message_handler(content_types=["text"])
def handle_text(message):
    global current_language, search_results
    user_id = message.from_user.id
    text = message.text.strip()

    # Проверка на режим sound
    if user_id in sound_mode:
        bot.send_chat_action(message.chat.id, 'record_audio')
        audio_path = text_to_speech(text, current_language)

        if audio_path:
            with open(audio_path, 'rb') as audio:
                bot.send_voice(message.chat.id, audio,
                               reply_markup=get_language_keyboard())
            os.unlink(audio_path)
        else:
            bot.send_message(message.chat.id,
                             language_texts[current_language]['sound_mode_error'],
                             reply_markup=get_language_keyboard())
        return

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


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.data.startswith("speak:"):
            search_id = call.data.split(":")[1]
            if search_id in search_results:
                text = search_results[search_id]['text']
                audio_path = text_to_speech(text, current_language)
                if audio_path:
                    with open(audio_path, 'rb') as audio:
                        bot.send_voice(call.message.chat.id, audio)
                    os.unlink(audio_path)
                else:
                    bot.send_message(call.message.chat.id,
                                     language_texts[current_language]['audio_error'])
            else:
                bot.send_message(call.message.chat.id,
                                 language_texts[current_language]['no_content'])

        elif call.data.startswith("runes:"):
            search_id = call.data.split(":")[1]
            if search_id in search_results:
                text = search_results[search_id]['text']
                # Simple runic conversion (just for demonstration)
                runic_text = text.replace('a', 'ᚨ').replace('b', 'ᛒ').replace('c', 'ᚲ').replace('d', 'ᛞ')
                bot.send_message(call.message.chat.id,
                                 f"Runic text:\n\n{runic_text}")
            else:
                bot.send_message(call.message.chat.id,
                                 language_texts[current_language]['no_content'])
    except Exception as e:
        print(f"Error in callback: {e}")
        bot.send_message(call.message.chat.id,
                         language_texts[current_language]['general_error'])
@bot.message_handler(commands=["Yarik"])
def handle_text(message):
    bot.send_message(message.chat.id, "Ярик лох")


if __name__ == '__main__':
    print("Bot is running...")
    bot.polling(none_stop=True)