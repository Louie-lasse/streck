from typing import Mapping
from . import Command

class Command_registry():

    def __init__(self) -> None:
        self._registry = {}

    def add(self, command: Command) -> None:
        self._registry[command.__cmd__()] = command
    
    def __iter__(self):
        return iter(self._registry.values())
    
    def __len__(self):
        return len(self._registry)
    
    def __getitem__(self, key):
        return self._registry[key]
    
    def __contains__(self, key):
        return key in self._registry
    
    def __str__(self):
        return '\n'.join([
            f"- {command}" for command in self._registry.values()
        ])
    
    def __repr__(self):
        return self.__str__()
    
    def merge(self, rep):
        combined = Command_registry()
        for command in self:
            combined.add(command)
        for command in rep:
            combined.add(command)
        return combined