from abc import ABC, abstractmethod

class Command(ABC):
    """Base class for all commands."""

    @abstractmethod
    def execute(self, user_id, args, say):
        """
        A custom command to execute for the slack bot
        """
        pass

    @abstractmethod
    def help(self):
        """
        Detailed help description for the specific command
        """
        pass

    @abstractmethod
    def __str__(self):
        """
        A simple, one-line, description of the function. Used by the `help` command
        """
        pass
