import argparse

import conllxi_reader
import file_util

START = "_start"


def train(training_path, tag_type):
    assert training_path is not None
    assert tag_type is not None

    sentences = conllxi_reader.read_conllxi(training_path)

    transition_prob = dict(dict())
    word_prob = dict(dict())
    tag_occurence = dict()

    for sentence in sentences:
        tokens = sentence.get_valid_tokens()

        for i in range(len(tokens)):

            word = tokens[i].get_representation()
            word_tag = tokens[i].get_data()[tag_type]
            if word not in word_prob:
                word_prob[word] = dict()

            if word_tag in word_prob[word]:
                word_prob[word][word_tag] += 1
            else:
                word_prob[word][word_tag] = 1

            if i == 0:
                before = START
            else:
                before = tokens[i - 1].get_data()[tag_type]

            if before not in transition_prob:
                transition_prob[before] = dict()

            if word_tag in transition_prob[before]:
                transition_prob[before][word_tag] += 1
            else:
                transition_prob[before][word_tag] = 1

            if word_tag in tag_occurence:
                tag_occurence[word_tag] += 1
            else:
                tag_occurence[word_tag] = 1

            if before == START:
                if START in tag_occurence:
                    tag_occurence[START] += 1
                else:
                    tag_occurence[START] = 1

    for before in transition_prob:
        for word_tag in transition_prob[before]:
            transition_prob[before][word_tag] = transition_prob[before][word_tag] / tag_occurence[before]

    for word in word_prob:
        for word_tag in word_prob[word]:
            word_prob[word][word_tag] = word_prob[word][word_tag] / tag_occurence[word_tag]

    file_util.write_dic(".transition_prob", transition_prob)
    file_util.write_dic(".word_prob", word_prob)

    # written_tr_prob = file_util.read_dic(".transition_prob")
    # written_word_prob = file_util.read_dic(".word_prob")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('path', help='Path of training data')
    parser.add_argument('--postag', action="store_true",
                        help='uses cpostag by default input --postag to switcg')
    parser.add_argument('--cpostag', action="store_true",
                        help='uses cpostag by default input --postag to switcg')

    opts = parser.parse_args()

    TRAINING_PATH = opts.path
    if opts.postag:
        TAGTYPE = 4
        print("Training " + TRAINING_PATH + " with postag...")
    else:
        print("Training " + TRAINING_PATH + " with cpostag...")
        TAGTYPE = 3

    train(TRAINING_PATH, TAGTYPE)
