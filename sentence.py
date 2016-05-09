from word import Word


class Sentence:
    def __init__(self, sentence_block):
        self._tokens = []
        for i in range(len(sentence_block)):
            word = Word(sentence_block[i])

            if not word.get_lemma() or word.get_lemma() == '_':
                if i != 0 and self._tokens[i - 1].get_form() == '_':
                    word.set_lemma(self._tokens[i - 1].get_lemma())
            self._tokens.append(word)

    def get_tokens(self):
        return self._tokens

    def get_valid_tokens(self):
        valids = []

        for item in self._tokens:
            if item.get_form() != "_":
                valids.append(item)

        return valids

    def get_human_sentence(self):
        sentence = ""

        for token in self.get_valid_tokens():
            sentence += " " + token.get_form()

        return sentence
