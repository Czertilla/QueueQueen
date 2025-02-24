import gzip
import os
import shutil
import glob
from logging.handlers import TimedRotatingFileHandler

class GzipTimedRotatingFileHandler(TimedRotatingFileHandler):
    """Ротирующий логгер с автоматическим сжатием gzip."""
    
    def doRollover(self):
        """Сжатие после ротации."""
        super().doRollover()
        
        for old_log in glob.glob(self.baseFilename + ".*"):
            if not old_log.endswith(".gz"):
                with open(old_log, "rb") as f_in:
                    with gzip.open(f"{old_log}.gz", "wb") as f_out:
                        shutil.copyfileobj(f_in, f_out)
                os.remove(old_log)
