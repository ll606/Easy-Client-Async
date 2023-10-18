import logging
import os
from datetime import datetime
from functools import partial
from types import MappingProxyType
from typing import Optional, Union, Dict
from typing_extensions import Literal
from uuid import uuid4


from .config import global_config


LogLevel = Optional[Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']]

class Logger:
    '''
        Attributes:
            loggers:
                all instances are stored in this dict
            
            level:
                the logging level: 
                    DEBUG, INFO, WARNING, ERROR, CRITICAL
            
            logpath:
                the folder storing log files.
            
            logfile:
                the filename for log files
        
        Arguments:
            name:
                the name for logger
            
            extra:
                the dict contains and only contains 
                two keys -> executor, task
                
        how to use:
            >>> lg = Logger(
            ...     name="test", 
            ...     extra={"executor": "test", "task": "test logger"}
            ... )
            >>> lg.debug("this will not be seen unless you set the level as debug")
            >>> lg.info("this is testing")
            >>> lg.error("oooops! something wrong!")
            >>> lg.critical("sorry! I have been crushed!")
    '''
    loggers: Dict[str, 'Logger'] = {}
    level: LogLevel = global_config['log_level']
    logpath: Optional[str] = global_config['log_path']
    logfile: Optional[str] = None
    
    def __init__(self, 
        name: Optional[str]=None,
        extra: Optional[Dict[str, str]] = None
    ) -> None:
        if name is not None and name in self.loggers:
            return self.loggers[name]
        
        self.name = 'unknown' if name is None else name
        if name is None:
            self._logger = logging.getLogger(self.name + str(uuid4()))
        else:
            self._logger = logging.getLogger(self.name)
        
        self._logger.setLevel(self.level.upper())
        self.format = (
            '%(asctime)s\t %(levelname)s\t '
            'Executor: "%(executor)s" \t'
            'Task: "%(task)s"\t '
            'Message: "%(message)s"'
        )
        
        self._formatter = logging.Formatter(self.format)
        if extra is None:
            extra = {'executor': 'unknown', 'task': 'unknown'}
        
        if self.logfile is None:
            self.__class__.logfile = '%s %s.txt' % (
                datetime.now().strftime('%Y-%m-%d %H.%M.%S'),
                name
            )
        
        logfile = self.__class__.logfile
        console_handler = logging.StreamHandler()
        if not os.path.isdir(self.logpath):
            os.mkdir(self.logpath)
        file_handler = logging.FileHandler(os.path.join(self.logpath, logfile))
        
        console_handler.setFormatter(self._formatter)
        file_handler.setFormatter(self._formatter)
        self._logger.addHandler(console_handler)
        self._logger.addHandler(file_handler)
        
        for level in ['debug', 'info', 'warning', 'error', 'critical']:
            setattr(
                self, level,
                partial(getattr(self._logger, level), extra=extra)
            )
        
        if self.name not in self.loggers:
            self.loggers[self.name] = self
            
    def add_handler(self, handler: logging.Handler):
        handler.setFormatter(self._formatter)
        self._logger.addHandler(handler)
    
    @classmethod
    def set_level(cls, level: LogLevel):
        for logger in cls.loggers:
            logger: 'Logger'
            logger._logger.setLevel(level)
            