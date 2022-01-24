import sys

from logbook import Logger, StreamHandler

LOG_NAME = "phimtools"

log_handler = StreamHandler(sys.stderr)
log_handler.push_application()
Log = Logger(LOG_NAME)

# other log
logger = Logger(LOG_NAME)
logger_cmd = Logger(LOG_NAME + "-commands")
logger_stdout = Logger(LOG_NAME + "-stdout")
