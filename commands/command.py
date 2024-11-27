from abc import ABC, abstractmethod

class Command(ABC):
    """Base class for all commands."""

    @abstractmethod
    def execute(self, user_ids : tuple[str,str], args : str, say):
        """
        A custom command to execute for the slack bot
        """

    @abstractmethod
    def help(self):
        """
        Detailed help description for the specific command
        """

    @abstractmethod
    def __str__(self):
        """
        A simple, one-line, description of the function. Used by the `help` command
        """