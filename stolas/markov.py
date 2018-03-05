from collections import namedtuple
import random

Word = namedtuple('Word', ['character', 'count'])


class ParseLengthError(Exception):
    pass


class NotParsedYetException(Exception):
    pass


class MarkovChain(object):
    """Hold the a chain in memory"""

    def __init__(self, order=4):
        """
        Create a new MarkovChain

        :param: order - Number of characters per word
        """

        self.order = int(order)

        if self.order <= 0:
            raise ValueError("Order must be greater than zero!")

        self._chain = {}
        self._start_words = []
        self._parsed = False
        self._existing_corpus = set()

    def _add_word_to_chain(self, word, new_character):

        if word not in self._chain:
            self._chain[word] = []

        for index, existing_words in enumerate(self._chain[word]):
            if existing_words.character == new_character:

                # Increment the existing character
                self._chain[word][index] = Word(
                    new_character,
                    existing_words.count + 1
                )

                return

        # Not found, add a new one
        self._chain[word].append(
            Word(new_character, 1)
        )

    def _get_random_word(self, key):
        """Get a weighted random Word from the chain"""

        possible_words = []

        for word in self._chain[key]:
            # HACK: Do this better
            for _ in range(word.count):
                possible_words.append(word.character)

        return random.choice(possible_words)

    def clean_text(self, raw_text):

        words = raw_text.split(" ")

        return " ".join(
            filter(lambda x: not x.startswith("@"), words)
        )

    def parse(self, raw_text):
        """Add text to the current chain.

        :param: raw_text - Input string"""

        safe_text = self.clean_text(raw_text)

        if safe_text in self._existing_corpus:
            return

        self._existing_corpus.add(safe_text)

        all_words = safe_text.split(" ")
        self._start_words.append(
            " ".join(all_words[:self.order])
        )

        self._parsed = True

        words = []

        for word in safe_text.split(" "):
            if word.startswith("@"):
                continue

            if len(words) == self.order:
                word_key = " ".join(words)
                self._add_word_to_chain(word_key, word)
                del words[0]
            words.append(word)

    def get_text(self, length=400):
        """Get text from this chain"""

        if not self._parsed:
            return ""

        if not self._chain.keys():
            return ""

        word_buffer = []
        current_length = 0

        # Start with a random key from the chain
        # Add it to the output
        # Take one of the Letters in values and use it
        # Then take the current latest

        key = random.choice(self._start_words)
        word_buffer.append(key)

        current_length += len(key)

        while len(word_buffer) < length:
            try:
                next_word = self._get_random_word(key)
                word_buffer.append(next_word)
                # HACK: Fix this later
                words = " ".join(word_buffer).split(" ")
                key = " ".join(words[-self.order:])
            except (KeyError, IndexError):
                break

        return " ".join(word_buffer)
