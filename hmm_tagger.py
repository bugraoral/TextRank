import argparse
import os

import conllxi_reader
import file_util

START = "_start"
TAG_SEPARATOR = "|"


def tag(data_file, output_file):
    assert data_file is not None
    assert output_file is not None

    tag_transition_prob = file_util.read_dic(".transition_prob")
    word_tag_prob = file_util.read_dic(".word_prob")

    output_text = []

    if os.path.exists(output):
        os.remove(output)

    sentences = conllxi_reader.read_conllxi(data_file)

    for sentence in sentences:
        tokens = sentence.get_valid_tokens()

        predicted_tags = get_tags(tokens, tag_transition_prob, word_tag_prob)

        for i in range(len(tokens)):
            output_text.append(tokens[i].get_form() + TAG_SEPARATOR + predicted_tags[i])
        output_text.append("\n")

    file_util.write_array(output_file, output_text)


def get_word_tag_prob(word_tag_probs, tag, token):
    if token.get_representation() in word_tag_probs:
        if tag in word_tag_probs[token.get_representation()]:
            return word_tag_probs[token.get_representation()][tag]
        else:
            # we have evidence that the given token has the given tag,thus 0 probability.
            return 0.0

    # if we are in this case, it means that we have not seen the word in training,
    # and we don't want to return 0 because it will end the tagging.
    # Intuitively if a word is unknown to me, I would look at the grammar to determine the most possible one.
    # So 1.0 is return to trust the grammar represented by tag transition prob matrix

    return 1.0


def get_safe_transition_prob(tag_transition_probs, from_tag, to_tag):
    if from_tag in tag_transition_probs and to_tag in tag_transition_probs[from_tag]:
        return tag_transition_probs[from_tag][to_tag]
    return 0


def get_tags(tokens, tag_transition_probs, word_tag_probs):
    viterbi = [0 for x in range(len(tokens))]

    postags = ['_' for x in range(len(tokens))]

    # Instantiation
    for tag in tag_transition_probs:
        if tag == START:
            continue
        posProb = get_safe_transition_prob(tag_transition_probs, START, tag) * get_word_tag_prob(word_tag_probs, tag,
                                                                                                 tokens[0])
        if posProb > viterbi[0]:
            viterbi[0] = posProb
            postags[0] = tag
    # Recursion
    for i in range(1, len(tokens)):
        posProb = 0
        for tag in tag_transition_probs:
            if tag == START:
                continue
            posProb = viterbi[i - 1] * get_safe_transition_prob(tag_transition_probs, postags[i - 1],
                                                                tag) * get_word_tag_prob(word_tag_probs,
                                                                                         tag,
                                                                                         tokens[i])
            if posProb > viterbi[i]:
                viterbi[i] = posProb
                postags[i] = tag

    return postags


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('path', help='Path of test data')
    parser.add_argument('output', help='output file')

    opts = parser.parse_args()

    data = opts.path
    output = opts.output

    tag(data, output)
