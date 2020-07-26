# import requests
import pprint
import telebot
import os
import re
# import ffmpeg

import db
from app_logger import get_logger
from face_detector import detect_faces_quantity
import settings



logger = get_logger(__name__)
tb = telebot.TeleBot(settings.BOT_TOKEN)


def download_file(file_id):
    file_path = tb.get_file(file_id).file_path
    downloaded_file = tb.download_file(file_path)
    return downloaded_file


@tb.message_handler(content_types=['audio', 'voice', 'document'])
def handle_docs_audio(message):
    try:
        if message.content_type == 'audio':
            file_id = message.audio.file_id
        elif message.content_type == 'voice':
            file_id = message.voice.file_id
        elif message.content_type == 'document' and re.match(r'audio', message.document.mime_type):
            file_id = message.document.file_id
        else:
            logger.info('Не определен тип аудио-контента.')
            return

        user_id = message.from_user.id
        downloaded_file = download_file(file_id)

        last_file_num = db.get_last_audio_num_by_user_id(user_id=user_id)
        next_file_num = int(last_file_num) + 1
        file_name = f'{user_id}_audio_message_{last_file_num}'

        with open(f'{settings.DIR_TO_SAVE_AUDIO_FILES}/{file_name}', 'wb') as new_file:
            new_file.write(downloaded_file)

        db.add_audio(user_id=user_id, file_id=file_id)

        sound_in_path = settings.DIR_TO_SAVE_AUDIO_FILES + "/" + file_name
        sampling_rate = 16000
        audio_format = "wav"
        sound_out_path = settings.DIR_TO_SAVE_CONVERTED_16KHZ_AUDIO_FILES + "/" + file_name

        os.system(f'ffmpeg -i "{sound_in_path}" -vn -ar {sampling_rate} -ac 2  -f {audio_format} "{sound_out_path}"')

    except Exception as e:
        logger.error('Ошибка.', exc_info=e)
        # bot.reply_to(message, e)


@tb.message_handler(content_types=['photo'])
def handle_images(message):
    try:
        user_id = message.from_user.id
        file_id = message.photo[len(message.photo)-1].file_id
        downloaded_file = download_file(file_id)
        if detect_faces_quantity(downloaded_file):
            with open(f'{settings.DIR_TO_SAVE_PHOTO_FILES}/{file_id}', 'wb') as new_file:
                new_file.write(downloaded_file)

            db.add_photo(user_id=user_id, file_id=file_id)

    except Exception as e:
        logger.error('Ошибка.', exc_info=e)
        # bot.reply_to(message, e)



def main():
    logger.info('Start AudioBot')

    # Создаем папки для хранения файлов
    os.makedirs(settings.DIR_TO_SAVE_AUDIO_FILES, exist_ok=True)
    os.makedirs(settings.DIR_TO_SAVE_CONVERTED_16KHZ_AUDIO_FILES, exist_ok=True)
    os.makedirs(settings.DIR_TO_SAVE_PHOTO_FILES, exist_ok=True)

    # Создаем базу данных
    db.init_db()

    tb.polling(none_stop=False, interval=0, timeout=20)

    logger.info('Stop AudioBot')


if __name__ == '__main__':
    main()
