import unittest
import mock
import os

from stolas.bot import StolasEbooks


class StolasEbooksAddTooTestCase(unittest.TestCase):
    """Tests for StolasEbooks.add_toot_to_corpus"""

    def _get_mocked_bot(self):

        head, _ = os.path.split(__file__)

        bot = StolasEbooks("test.conf")
        bot.markov = mock.MagicMock()
        bot.connect_to_sqlite = mock.MagicMock()
        bot.mastodon = mock.MagicMock()
        return bot

    def test_does_add_valid_toot(self):

        bot = self._get_mocked_bot()

        test_toot = {
            "content": "Test TOOT",
            "id": 7,
            "in_reply_to_id": "greg",
            "reblog": None,
            "spoiler_text": None
        }

        result = bot.add_toot_to_corpus(test_toot)
        self.assertTrue(result)

    def test_does_add_replies(self):
        # I changed my mind and want to add replies after all

        bot = self._get_mocked_bot()

        test_toot = {
            "content": "Test TOOT",
            "id": 7,
            "in_reply_to_id": "greg",
            "reblog": None,
            "spoiler_text": None
        }

        result = bot.add_toot_to_corpus(test_toot)
        self.assertTrue(result)

    def test_does_not_add_boosts(self):

        bot = self._get_mocked_bot()

        test_toot = {
            "content": "Test TOOT",
            "id": 7,
            "in_reply_to_id": "",
            "reblog": {
                "values": "yes"
            },
            "spoiler_text": None
        }

        result = bot.add_toot_to_corpus(test_toot)
        self.assertFalse(result)

    def test_does_not_add_toots_with_cw(self):

        bot = self._get_mocked_bot()

        test_toot = {
            "content": "Test TOOT",
            "id": 7,
            "in_reply_to_id": "",
            "reblog": None,
            "spoiler_text": "Lewd"
        }

        result = bot.add_toot_to_corpus(test_toot)
        self.assertFalse(result)
