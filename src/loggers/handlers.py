import gzip
import os
import shutil
import glob
from logging.handlers import TimedRotatingFileHandler


class GzipTimedRotatingFileHandler(TimedRotatingFileHandler):
    """Timed rotating file handler with automatic gzip compression."""

    def doRollover(self):
        """Compresses the rotated log file using gzip."""
        super().doRollover()

        for old_log in glob.glob(self.baseFilename + ".*"):
            if not old_log.endswith(".gz"):
                with open(old_log, "rb") as f_in:
                    with gzip.open(f"{old_log}.gz", "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove(old_log)