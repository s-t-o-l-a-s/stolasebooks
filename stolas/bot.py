from .markov import MarkovChain

import ananas
import sqlite3

CORPUS_FILEPATH = "_corpus.sqlite3"


class StolasEbooks(ananas.PineappleBot):
    """StolasEbooks class that contains the bot"""

    def connect_to_sqlite(self):
        """Returns a connection to sqlite

        Please make sure to commit and close this!"""

        return sqlite3.connect(CORPUS_FILEPATH)

    def start(self):

        db_conn = self.connect_to_sqlite()

        db_conn.execute(
            """CREATE TABLE IF NOT EXISTS toots (
                toot_id INT NOT NULL UNIQUE,
                text_content TEXT NOT NULL
            );
            """
        )

        db_conn.commit()

        self.markov = MarkovChain(self.config.order)

        self.get_all_toots()

        self.populate_chain_from_database()

    def populate_chain_from_database(self):
        """Parse all the toots in the database"""

        print("Populating!")

        db_conn = self.connect_to_sqlite()

        cursor = db_conn.cursor()

        cursor.execute("SELECT text_content FROM toots")

        toot_result = cursor.fetchone()
        while toot_result:
            self.markov.parse(toot_result[0])
            toot_result = cursor.fetchone()

        db_conn.close()

        print("DONE!")

    def add_toot(self, toot_dict):
        """Commit a toot_dict to the database
        and add it to the chain
        """

    def get_all_toots(self):

        users = self.mastodon.account_search(
            self.config.ebooks_user
        )

        assert len(users) == 1

        self._get_page(users[0])

    def get_recent_toots(self):

        users = self.mastodon.account_search(
            self.config.ebooks_user
        )

        assert len(users) == 1

        statuses = self.mastodon.account_statuses(
            id=users[0]
        )

        for status in statuses:
            self.add_toot_to_corpus(status)
            self.markov.parse(status)

    def _get_page(self, user, **kwargs):

        statuses = self.mastodon.account_statuses(
            id=user,
            **kwargs
        )

        for status in statuses:

            if status.get("_pagination_next"):
                self._get_page(
                    user,
                    max_id=status["_pagination_next"]["max_id"]
                )

            self.add_toot_to_corpus(status)

    def add_toot_to_corpus(self, toot):

        if toot['reblog']:
            return False

        if toot['spoiler_text']:
            return False

        text_content = ananas.html_strip_tags(toot['content'])

        db_conn = self.connect_to_sqlite()
        cursor = db_conn.cursor()

        try:
            toot_input = (toot['id'], text_content)
            cursor.execute("INSERT INTO toots VALUES (?, ?)", toot_input)
            db_conn.commit()
        except sqlite3.IntegrityError:
            pass  # Toot is already in DB, nevermind

        return True

    @ananas.interval(30)
    def update_markov(self):
        self.get_recent_toots()

    @ananas.interval(60 * 42)
    def toot(self):
        status = self.markov.get_text(300)
        self.mastodon.status_post(
            status,
            in_reply_to_id=None,
        )

    @ananas.reply
    def reply_toot(self, mention, user):
        status = self.markov.get_text(300)
        self.mastodon.status_post(
            '@{0} {1}'.format(user.acct, status),
            in_reply_to_id=mention,
        )
