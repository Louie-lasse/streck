from abc import ABC, abstractmethod
import os

class Command(ABC):
    """Base class for all commands."""

    _ADMIN = os.getenv("ADMIN")

    def __str__(self):
        """
        A simple, one-line, description of the function. Used by the `help` command
        """
        return f"`{self.__cmd__()}`: {self.description()}"

    def __repr__(self):
        return self.__cmd__()

    @abstractmethod
    def execute(self, user_ids, args : str, say):
        """
        How the command should be executed
        """

    @abstractmethod
    def help(self):
        """
        Detailed help description for the specific command
        """

    @abstractmethod
    def description(self):
        """
        A short, one line, description of the command
        """
        pass
    
    @abstractmethod
    def __cmd__(self):
        """
        The command name. The accutal command used by the user
        """
        pass
