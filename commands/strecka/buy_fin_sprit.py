from .base_strecka import Strecka

class FinSprit(Strecka):
    def __init__(self):
        super().__init__(42, 0.5)

    def help(self):
        return "Antal cl finsprit du vill sträcka. "\
                "Notera att vanliga sträckkoden är för 2 cl. "\
                f"Skriv e.g. `{self.__cmd__()} 12` för en 12:a"

    def description(self):
        return "Sträcka finsprit (cl)"

    def __cmd__(self):
        return "fin"

    def usage(self):
        return f"{self.__cmd__()} [<antal cl>]"
