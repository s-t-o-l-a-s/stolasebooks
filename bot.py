import ananas


class StolasEbooks(ananas.PineappleBot):
    """StolasEbooks class that contains the bot"""

    @ananas.interval(1)
    def toot(self):
        self.mastodon.status_post(
            status="Hello World! This should have a CW and be unlisted!",
            sensitive=True,
            visibility="unlisted",
            spoiler_text="Test CW!!"
        )
