import unittest
from stolas.markov import MarkovChain, Letter, ParseLengthError


class MarkovTestCase(unittest.TestCase):

    def test_parse_valid_text(self):
        # Parse method should set .chain correctly

        markov = MarkovChain()
        self.assertEqual(markov._chain, {})

        input_text = "abc"
        markov.parse(input_text, order=1)

        self.assertEqual(
            set(markov._chain.keys()),
            set(['a', 'b'])
        )

        self.assertEqual(
            markov._chain['a'],
            [Letter('b', 1)]
        )

        self.assertEqual(
            markov._chain['b'],
            [Letter('c', 1)]
        )

    def test_parse_fails_when_input_too_short(self):
        # If order is less than the length of the string
        # then a parse must fail with a ParseLengthError

        markov = MarkovChain()

        with self.assertRaises(ParseLengthError):
            markov.parse('', order=1)
            markov.parse('', order=2)
            markov.parse('', order=3)
            markov.parse('', order=4)

            markov.parse('a', order=2)
            markov.parse('a', order=3)
            markov.parse('a', order=4)

            markov.parse('ab', order=3)
            markov.parse('ab', order=3)

            markov.parse('abc', order=4)

    def test_multiple_parse_calls(self):
        # Calling parse more than one should
        # append to the existing chain
        # but each call should be seperate

        markov = MarkovChain()
        self.assertEqual(markov._chain, {})

        input_text_one = "abc"
        input_text_two = "def"

        # Note that c does NOT go to d
        markov.parse(input_text_one, order=1)
        markov.parse(input_text_two, order=1)

        self.assertEqual(
            set(markov._chain.keys()),
            set(['a', 'b', 'd', 'e'])
        )

        self.assertEqual(
            markov._chain['a'],
            [Letter('b', 1)]
        )

        self.assertEqual(
            markov._chain['b'],
            [Letter('c', 1)]
        )

        self.assertEqual(
            markov._chain['d'],
            [Letter('e', 1)]
        )

        self.assertEqual(
            markov._chain['e'],
            [Letter('f', 1)]
        )

    def test_parse_newlinest(self):
        # Newlines must be treated like any other character

        markov = MarkovChain()
        self.assertEqual(markov._chain, {})

        input_text = "a\nb\nc"
        markov.parse(input_text, order=1)

        self.assertEqual(
            set(markov._chain.keys()),
            set(['a', 'b', '\n'])
        )

        self.assertEqual(
            markov._chain['a'],
            [Letter('\n', 1)]
        )

        self.assertEqual(
            markov._chain['b'],
            [Letter('\n', 1)]
        )

        self.assertEqual(
            markov._chain['\n'],
            [Letter('b', 1), Letter('c', 1)]
        )
