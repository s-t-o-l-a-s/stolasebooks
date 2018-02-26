import ananas
import os
from .markov import MarkovChain


class StolasEbooks(ananas.PineappleBot):
    """StolasEbooks class that contains the bot"""

    def start(self):

        self.markov = MarkovChain(self.config.order)
        self._max_status_id = 0

        if not os.path.isdir(self.config.corpus_folder):
            raise ValueError("No folder at {}".format(
                self.config.corpus_folder))

        self.last_page = None

    def get_toots(self):

        users = self.mastodon.account_search(
            self.config.ebooks_user
        )

        assert len(users) == 1

        if not self.last_page:
            statuses = self.mastodon.account_statuses(
                id=users[0],
                exclude_replies=True
            )
        else:
            statuses = self.mastodon.fetch_next(
                self.last_page
            )

        self.last_page = statuses

        for status in statuses:
            # self._max_status_id = max(
            #     self._max_status_id,
            #     status['id']
            # )

            self.add_toot_to_corpus(status)

    def add_toot_to_corpus(self, toot):

        if toot['in_reply_to_id']:
            print("Nevermind")
            return

        if toot['reblog']:
            print("It's not OC, skipping")
            return

        text_content = ananas.html_strip_tags(toot['content'])

        self.markov.parse(text_content)

    @ananas.interval(1)
    def toot(self):
        print("BANG!")
        self.get_toots()
        # print(self.markov.get_text(300))
