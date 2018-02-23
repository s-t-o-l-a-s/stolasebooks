from collections import namedtuple

Letter = namedtuple('Letter', ['character', 'count'])


class ParseLengthError(Exception):
    pass


class MarkovChain(object):
    """Hold the a chain in memory"""

    def __init__(self):
        self._chain = {}

    def _add_word_to_chain(self, char_buffer, new_character):
        word = "".join(char_buffer)

        if word not in self._chain:
            self._chain[word] = []

        for index, existing_letters in enumerate(self._chain[word]):
            if existing_letters.character == new_character:

                # Increment the existing character
                self._chain[word][index] = Letter(
                    new_character,
                    existing_letters.count
                )

                return

        # Not found, add a new one
        self._chain[word].append(
            Letter(new_character, 1)
        )

    def parse(self, text, order=4):
        """Add text to the current chain.

        :param: text - Input string
        :param: order - Number of characters per word"""

        char_buffer = []

        if len(text) < order:
            raise ParseLengthError()

        for ii in text:
            if len(char_buffer) == order:
                self._add_word_to_chain(char_buffer, ii)
                del char_buffer[0]

            char_buffer.append(ii)

    def get_text(self, length=None):
        """Get text from this chain"""
