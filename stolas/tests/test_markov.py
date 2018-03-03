import unittest
from stolas.markov import MarkovChain, Word


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

        input_text = "a b c"
        markov.parse(input_text)

        self.assertEqual(
            set(markov._chain.keys()),
            set(['a', 'b'])
        )

        self.assertEqual(
            markov._chain['a'],
            [Word('b', 1)]
        )

        self.assertEqual(
            markov._chain['b'],
            [Word('c', 1)]
        )

    def test_at_sign_not_parsed(self):
        # In order to avoid tooting random people
        # the @ character must never enter the chain
        # and should be ignored

        markov = MarkovChain(order=1)
        self.assertEqual(markov._chain, {})

        input_text = "a b @d c"
        markov.parse(input_text)

        self.assertEqual(
            set(markov._chain.keys()),
            set(['a', 'b'])
        )

        self.assertEqual(
            markov._chain['a'],
            [Word('b', 1)]
        )

        self.assertEqual(
            markov._chain['b'],
            [Word('c', 1)]
        )

    def test_multiple_parse_calls(self):
        # Calling parse more than one should
        # append to the existing chain
        # but each call should be seperate

        markov = MarkovChain(order=1)
        self.assertEqual(markov._chain, {})

        input_text_one = "a b c"
        input_text_two = "d e f"

        # Note that c does NOT go to d
        markov.parse(input_text_one)
        markov.parse(input_text_two)

        self.assertEqual(
            set(markov._chain.keys()),
            set(['a', 'b', 'd', 'e'])
        )

        self.assertEqual(
            markov._chain['a'],
            [Word('b', 1)]
        )

        self.assertEqual(
            markov._chain['b'],
            [Word('c', 1)]
        )

        self.assertEqual(
            markov._chain['d'],
            [Word('e', 1)]
        )

        self.assertEqual(
            markov._chain['e'],
            [Word('f', 1)]
        )

    def test_parse_newlinest(self):
        # Newlines must be treated like any other character

        markov = MarkovChain(order=1)
        self.assertEqual(markov._chain, {})

        input_text = "a \nb \nc\nAAA end"
        markov.parse(input_text)

        self.assertEqual(
            set(markov._chain.keys()),
            set(['a', '\nb', '\nc\nAAA'])
        )

        self.assertEqual(
            markov._chain['a'],
            [Word('\nb', 1)]
        )

        self.assertEqual(
            markov._chain['\nb'],
            [Word('\nc\nAAA', 1)]
        )

    def test_order_four_input(self):
        input_text = ("According to all known laws of aviation,"
                      "there is no way a bee should be able to fly.")

        markov = MarkovChain(order=4)

        markov.parse(input_text)

        self.assertIn("According to all known", markov._chain.keys())
        self.assertEqual(
            markov._chain["According to all known"],
            [Word("laws", 1)]
        )

        self.assertIn("is no way a", markov._chain.keys())
        self.assertEqual(
            markov._chain["is no way a"],
            [Word("bee", 1)]
        )

        self.assertIn("should be able to", markov._chain.keys())
        self.assertEqual(
            markov._chain["should be able to"],
            [Word("fly.", 1)]
        )

    def test_duplicate_parsing_files(self):
        input_text = ("According to all known laws of aviation,"
                      "there is no way a bee should be able to fly.")

        markov = MarkovChain(order=4)

        markov.parse(input_text)
        markov.parse(input_text)
        markov.parse(input_text)
        markov.parse(input_text)

        self.assertIn("According to all known", markov._chain.keys())
        self.assertEqual(
            markov._chain["According to all known"],
            [Word("laws", 1)]
        )

        self.assertIn("is no way a", markov._chain.keys())
        self.assertEqual(
            markov._chain["is no way a"],
            [Word("bee", 1)]
        )

        self.assertIn("should be able to", markov._chain.keys())
        self.assertEqual(
            markov._chain["should be able to"],
            [Word("fly.", 1)]
        )


class MarkovChainRandomWordTestCase(unittest.TestCase):
    """Tests for MarkovChain._get_random_word"""

    def test_single_option(self):

        markov = MarkovChain()
        markov._chain = {
            'START': [
                Word('A', 1)
            ]
        }

        for _ in range(1000):
            letter = markov._get_random_word('START')
            self.assertEqual(letter, 'A')

    def test_even_odds(self):

        markov = MarkovChain()
        markov._chain = {
            'START': [
                Word('A', 10),
                Word('B', 10)
            ]
        }

        a_count = 0
        b_count = 0
        for _ in range(10000):
            letter = markov._get_random_word('START')

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
                Word('A', 10),
                Word('B', 1)
            ]
        }

        a_count = 0
        b_count = 0
        for _ in range(10000):
            letter = markov._get_random_word('START')

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

    def test_get_text_length(self):

        markov = MarkovChain(order=4)
        markov.parse("a b c d e f g")

        output = markov.get_text(length=200)
        self.assertGreaterEqual(len(output), 200)

    def test_run_on_bug(self):
        # There is a bug causing the ends of sentences
        # to get mauled

        markov = MarkovChain(order=2)
        markov.parse("a b a b a b a b a b")

        output = markov.get_text(1000)
        self.assertNotIn("ab", output)


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
