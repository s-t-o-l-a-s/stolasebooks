import ananas


class StolasEbooks(ananas.PineappleBot):
    """StolasEbooks class that contains the bot"""

    @ananas.interval(1)
    def toot(self):
        print("BANG!")
