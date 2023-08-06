import os
import sys
from datetime import datetime

class Logger:
    """A simple logger class"""

    def __init__(self, name, logToConsole = True, path = None):
        """Initializes the logger"""
        self._name = name
        self._path = path
        self._logToConsole = logToConsole

    def Log(self, message):
        """Logs a message in format [name] [timestamp] [message]"""
        message = f'[{self._name}] [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {message}'
        if self._logToConsole:
            print(message)
        if self._path is not None:
            with open(self._path, 'a') as f:
                f.write(message + '\n')
        
        