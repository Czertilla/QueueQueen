import logging
import traceback
# from asyncio import coroutine


class Exceptor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def traceback(self):
        self.logger.error(traceback.format_exc())

    def aiotect(self, coroutine):
        async def protected(*args, **kwargs):
            try:
                return await coroutine(*args, **kwargs)
            except Exception as e:
                logger = logging.getLogger(coroutine.__module__)
                logger.error("%s coroutine crushed by: \n\t%s",
                             coroutine.__name__, e)
                self.traceback()
        return protected

    def protect(self, func: "function"):
        def protected(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger = logging.getLogger(func.__module__)
                logger.error("%s function crushed by: \n\t%s",
                             func.__name__, e)
                self.traceback()
        return protected
