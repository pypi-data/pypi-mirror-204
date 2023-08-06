from .database.load_db import LoadDatabase as load_database
from .files.load_flat_files import LoadFlatFile as load_flat_file

# initialize the logging
import logging
logger = logging.getLogger(__name__)

handler = logging.StreamHandler()
stream_format = "%(levelname)s %(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
set_stream_format = logging.Formatter(stream_format)
handler.setFormatter(set_stream_format)
logger.addHandler(handler)

logger.setLevel(logging.DEBUG)