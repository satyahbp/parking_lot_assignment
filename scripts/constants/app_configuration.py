import os
import configparser

config = configparser.ConfigParser()
config.read("conf/application.conf")

LOG_SECTION = "LOG"
MONGO_SECTION = "MONGO"

# logging
LOG_NAME = config.get(LOG_SECTION, "log_name")
LOG_BASE_PATH = config.get(LOG_SECTION, "log_path")
LOG_FILE_NAME = config.get(LOG_SECTION, "file_name")
LOG_LEVEL = config.get(LOG_SECTION, "level")
LOG_MAX_FILE_SIZE = config.get(LOG_SECTION, "max_file_size")
LOG_MAX_FILE_BACKUPS = config.get(LOG_SECTION, "max_backup")
LOG_HANDLERS = config.get(LOG_SECTION, "handlers")


# mongo
MONGO_HOST = os.environ.get("MONGO_HOST", config.get(MONGO_SECTION, "mongo_host"))
MONGO_PORT = os.environ.get("MONGO_PORT", config.get(MONGO_SECTION, "mongo_port"))
PARKING_DB = config.get(MONGO_SECTION, "parking_db")
PARKING_COLLECTION = config.get(MONGO_SECTION, "parking_collection")