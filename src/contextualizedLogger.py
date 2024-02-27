from contextvars import ContextVar
import logging


class LoggerContext:
    id_: ContextVar[str] = ContextVar("req_id")

    @property
    def id(self) -> str:
        try:
            return self.id_.get()
        except LookupError:
            return "0"

    @id.setter
    def id(self, value: str):
        self.id_.set(value)


logger_context = LoggerContext()


class ContextualizedHandler(logging.StreamHandler):
    def emit(self, record: logging.LogRecord):
        record.message = f"{logger_context.id} {record.message}"
        super().emit(record)


def configure_logger():
    logger = logging.getLogger("contextualized-logger")
    logger.setLevel(logging.INFO)
    handler = ContextualizedHandler()
    logger.addHandler(handler)

