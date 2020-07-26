import os
import logging

BOT_TOKEN = os.getenv('BOT_TOKEN')

DIR_TO_SAVE_AUDIO_FILES = os.getcwd() + '/AUDIO_FILES'
DIR_TO_SAVE_CONVERTED_16KHZ_AUDIO_FILES = DIR_TO_SAVE_AUDIO_FILES + '/converted_16kHz'
DIR_TO_SAVE_PHOTO_FILES = os.getcwd() + '/PHOTO_FILES'


#logger settings
LOGGING_LEVEL = logging.DEBUG
COSOLE_FORMATTER = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt='%H:%M:%S')
FILE_FORMATTER = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt='%H:%M:%S')
LOG_FILE = "my_app.log"


#db settings
DATABASE_NAME = "audio_info.db"