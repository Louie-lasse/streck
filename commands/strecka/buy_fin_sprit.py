from .base_strecka import Strecka

class FinSprit(Strecka):
    def __init__(self):
        super().__init__(42)

    def help(self):
        return "Antal 2cl finsprit du vill sträcka. "\
                f"Skriv e.g. `{self.__cmd__()} 6` för en 12:a"

    def description(self):
        return "Sträcka finsprit (2cl)"

    def __cmd__(self):
        return "fin"

    def usage(self):
        return f"{self.__cmd__()} [<antal 2cl>]"
