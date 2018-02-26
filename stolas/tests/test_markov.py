import unittest
from stolas.markov import MarkovChain, Letter, ParseLengthError


class MarkovChainParseTestCase(unittest.TestCase):
    """Tests for MarkovChain.parse"""

    def test_internal_parsed_flag_set(self):
        # Calling parse method should set _parsed to True

        markov = MarkovChain(order=1)
        self.assertEqual(markov._parsed, False)
        markov.parse("It is a truth universally acknowledged, "
                     "that a single man in possession of a good "
                     "fortune must be in want of a wife.")
        self.assertEqual(markov._parsed, True)

    def test_parse_valid_text(self):
        # Parse method should set .chain correctly

        markov = MarkovChain(order=1)
        self.assertEqual(markov._chain, {})

        input_text = "abc"
        markov.parse(input_text)

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

    def test_at_sign_not_parsed(self):
        # In order to avoid tooting random people
        # the @ character must never enter the chain
        # and should be ignored

        markov = MarkovChain(order=1)
        self.assertEqual(markov._chain, {})

        input_text = "ab@c"
        markov.parse(input_text)

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

        markov = MarkovChain(order=1)

        with self.assertRaises(ParseLengthError):
            markov.parse('')

    def test_multiple_parse_calls(self):
        # Calling parse more than one should
        # append to the existing chain
        # but each call should be seperate

        markov = MarkovChain(order=1)
        self.assertEqual(markov._chain, {})

        input_text_one = "abc"
        input_text_two = "def"

        # Note that c does NOT go to d
        markov.parse(input_text_one)
        markov.parse(input_text_two)

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

    def test_duplicate_input_not_parsed(self):
        # Calling parse more than one should
        # append to the existing chain
        # but each call should be seperate

        markov = MarkovChain(order=1)
        self.assertEqual(markov._chain, {})

        input_text = "abacab"

        # Note that c does NOT go to d
        markov.parse(input_text)

        self.assertEqual(
            markov._chain['a'],
            [Letter('b', 2), Letter('c', 1)]
        )

    def test_parse_newlinest(self):
        # Newlines must be treated like any other character

        markov = MarkovChain(order=1)
        self.assertEqual(markov._chain, {})

        input_text = "a\nb\nc"
        markov.parse(input_text)

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

    def test_order_four_input(self):
        input_text = ("According to all known laws of aviation,"
                      "there is no way a bee should be able to fly.")

        markov = MarkovChain(order=4)

        markov.parse(input_text)

        self.assertIn("Acco", markov._chain.keys())
        self.assertEqual(
            markov._chain["Acco"],
            [Letter("r", 1)]
        )

        self.assertIn("of a", markov._chain.keys())
        self.assertEqual(
            markov._chain["of a"],
            [Letter("v", 1)]
        )

        self.assertIn(" fly", markov._chain.keys())
        self.assertEqual(
            markov._chain[" fly"],
            [Letter(".", 1)]
        )


class MarkovChainRandomLetterTestCase(unittest.TestCase):
    """Tests for MarkovChain._get_random_letter"""

    def test_single_option(self):

        markov = MarkovChain()
        markov._chain = {
            'START': [
                Letter('A', 1)
            ]
        }

        for _ in range(1000):
            letter = markov._get_random_letter('START')
            self.assertEqual(letter, 'A')

    def test_even_odds(self):

        markov = MarkovChain()
        markov._chain = {
            'START': [
                Letter('A', 10),
                Letter('B', 10)
            ]
        }

        a_count = 0
        b_count = 0
        for _ in range(10000):
            letter = markov._get_random_letter('START')

            if letter == 'A':
                a_count += 1
            elif letter == 'B':
                b_count += 1
            else:
                self.fail("Expected 'A' or 'B' got {0}".format(
                    letter
                ))

        self.assertEqual(a_count + b_count, 10000)
        self.assertGreaterEqual(a_count, 4500)
        self.assertLessEqual(a_count, 5500)

    def test_10_1_odds(self):

        markov = MarkovChain()
        markov._chain = {
            'START': [
                Letter('A', 10),
                Letter('B', 1)
            ]
        }

        a_count = 0
        b_count = 0
        for _ in range(10000):
            letter = markov._get_random_letter('START')

            if letter == 'A':
                a_count += 1
            elif letter == 'B':
                b_count += 1
            else:
                self.fail("Expected 'A' or 'B' got {0}".format(
                    letter
                ))

        self.assertEqual(a_count + b_count, 10000)
        self.assertGreaterEqual(a_count, 9000)


class MarkovChainGetTextTestCase(unittest.TestCase):
    """Tests for MarkovChain.get_text"""

    def test_get_text_null_input(self):
        # If we have nothing in _chain then we
        # want to return an empty string

        markov = MarkovChain(order=4)
        self.assertEqual(markov._chain, {})
        self.assertEqual(markov._parsed, False)

        output = markov.get_text()
        self.assertEqual(output, "")

    def test_get_text_input(self):
        # Parse method should set .chain correctly

        markov = MarkovChain(order=1)
        markov.parse("aba")

        self.assertEqual(markov._parsed, True)

        output = markov.get_text(length=10)
        self.assertIn("ab", output)
        self.assertIn("ba", output)

    def test_get_text_length(self):

        markov = MarkovChain(order=4)
        markov.parse("ermeimfoiefmqmfimeqofeqmfe")

        output = markov.get_text(length=200)
        self.assertGreaterEqual(len(output), 200)


class MarkovChainErrorTestCase(unittest.TestCase):

    def test_order_zero_raises_exception(self):
        with self.assertRaises(ValueError):
            MarkovChain(order=0)

    def test_order_negative_raises_exception(self):
        with self.assertRaises(ValueError):
            MarkovChain(order=-1)

    def test_order_string_raises_exception(self):
        with self.assertRaises(ValueError):
            MarkovChain(order="four")
