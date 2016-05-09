class Word:
    def __init__(self, token_line):
        self._data = token_line.split("\t")

    def get_form(self):
        return self._data[1]

    def get_lemma(self):
        return self._data[2]

    def get_cpost_tag(self):
        return self._data[3]

    def get_post_tag(self):
        return self._data[4]

    def get_data(self):
        return self._data

    def set_lemma(self, lemma):
        self._data[2] = lemma

    def get_representation(self):
        lemma = self.get_lemma()

        if lemma != '_':
            return lemma

        return self.get_form()
