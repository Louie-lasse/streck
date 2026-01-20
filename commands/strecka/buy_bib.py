from .base_strecka import Strecka

class Bib(Strecka):
    def __init__(self):
        super().__init__(41)

    def help(self):
        return "Antal 2cl bibsprit du vill sträcka. "\
                f"Skriv e.g. `{self.__cmd__()} 6` för en 12:a"

    def description(self):
        return "Sträcka bib sprit (2cl)"

    def __cmd__(self):
        return "bib"

    def usage(self):
        return f"{self.__cmd__()} [<antal 2cl>]"
