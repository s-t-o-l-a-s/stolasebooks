import unittest
import mock

from stolas.bot import StolasEbooks


class StolasEbooksAddTooTestCase(unittest.TestCase):
    """Tests for StolasEbooks.add_toot_to_corpus"""

    def test_does_not_add_replies(self):
        # Parse method should set .chain correctly

        bot = StolasEbooks("test.cfg")
        bot.markov = mock.MagicMock()

        test_toot = {
            "in_reply_to_id": "greg"
        }

        bot.add_toot_to_corpus(test_toot)
        bot.markov.parse.assert_not_called()

    def test_does_not_add_boosts(self):
        # Parse method should set .chain correctly

        bot = StolasEbooks("test.cfg")
        bot.markov = mock.MagicMock()

        test_toot = {
            "in_reply_to_id": "",
            "reblog": {
                "values": "yes"
            }
        }

        bot.add_toot_to_corpus(test_toot)
        bot.markov.parse.assert_not_called()
