"""
Module for containing different slackbot commands
"""

from .command import Command
from .buy_beer import Beer
from .buy_cider import Cider
from .buy_soda import Soda
from .list_users import List_Users
from .update import Update
from .connect import Connect
from .skuld import Skuld
from .strecklista import Strecklista
from .whois import Who_Is
from .whoami import Whoami
from .request import Request
from .say import Say
from .whereis import Where_Is

from .command_registry import Command_registry
