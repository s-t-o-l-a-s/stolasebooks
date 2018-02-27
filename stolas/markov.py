from collections import namedtuple
import random

Letter = namedtuple('Letter', ['character', 'count'])


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
        self._parsed = False

    def _add_word_to_chain(self, word, new_character):

        if word not in self._chain:
            self._chain[word] = []

        for index, existing_letters in enumerate(self._chain[word]):
            if existing_letters.character == new_character:

                # Increment the existing character
                self._chain[word][index] = Letter(
                    new_character,
                    existing_letters.count + 1
                )

                return

        # Not found, add a new one
        self._chain[word].append(
            Letter(new_character, 1)
        )

    def _get_random_letter(self, key):
        """Get a weighted random Letter from the chain"""

        possible_letters = []

        for letter in self._chain[key]:
            # HACK: Do this better
            for _ in range(letter.count):
                possible_letters.append(letter.character)

        return random.choice(possible_letters)

    def parse(self, text):
        """Add text to the current chain.

        :param: text - Input string"""

        self._parsed = True

        words = []

        for word in text.split(" "):
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

        text = ""
        while len(text) < length:
            text += self._get_text(length - len(text))

        return text

    def _get_text(self, length):
        char_buffer = []
        current_length = 0

        # Start with a random key from the chain
        # Add it to the output
        # Take one of the Letters in values and use it
        # Then take the current latest

        key = random.choice(
            list(self._chain.keys())
        )
        char_buffer.append(key)

        current_length += len(key)

        while len(char_buffer) < length:
            try:
                next_character = self._get_random_letter(key)
                char_buffer.append(next_character)
                key = "".join(char_buffer)[-self.order:]
            except (KeyError, IndexError):
                return "".join(char_buffer)

        return "".join(char_buffer)
