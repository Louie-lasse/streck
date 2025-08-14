from .strecka import Strecka

class Bib(Strecka):
    def __init__(self):
        super().__init__(0, 0.5)
        # todo replace `0` with the actual product ID for bibsprit

    def help(self):
        return "Antal cl bibsprit du vill sträcka. "\
                "Notera att vanliga sträckkoden är för 2 cl. "\
                f"Skriv e.g. `{self.__cmd__()} 12` för en 12:a"

    def description(self):
        return "Sträcka bib sprit (cl)"

    def __cmd__(self):
        return "bib"

    def usage(self):
        return f"{self.__cmd__()} [<antal cl>]"
