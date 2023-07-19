import logging
from logging import LogRecord
from pywebio.output import get_scope, put_text
from typing import Optional


class WebIOLoggingHandler(logging.Handler):

    def __init__(self, scope: Optional[str] = None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if scope is None:
            scope = get_scope()
        self.scope = scope
        self.colormap = {
            'DEBUG': 'rgba(100, 100, 100, 0.8)',
            'INFO': 'rgba(0, 0, 100, 0.8)',
            'WARNING': 'rgba(131, 84, 0, 0.8)',
            'ERROR': 'rgba(200, 0, 0, 1)',
            'CRITICAL': 'rgba(255, 0, 0, 1)'
        }

    def emit(self, record: LogRecord) -> None:
        msg: str = self.format(record)
        level: str = record.levelname
        put_text(msg, scope=self.scope).style(
            'color: %s' % self.colormap.get(
                level, 'rgba(0, 0, 0, 1)'
            )
        )