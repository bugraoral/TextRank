import os
import re
import string
import file_util

START = "_start"
TAG_SEPARATOR = "|"

PUNCTUATIONS = "r''"


def tag(data_file, output_file, vocabulary: dict ,tag_transition_prob, word_tag_prob):
    assert data_file is not None
    assert output_file is not None

    if not tag_transition_prob:
        print("Reading tag_transition_prob")
        tag_transition_prob = file_util.read_dic(".transition_prob")

    if not word_tag_prob:
        print("Reading word_tag_prob")
        word_tag_prob = file_util.read_dic(".word_prob")

    punctuation = re.compile('[%s]' % re.escape(string.punctuation))
    punctuation_without_apostrophe = re.compile('[%s]^\'' % re.escape(string.punctuation))
    output_text = []

    if os.path.exists(output_file):
        os.remove(output_file)

    sentences = file_util.get_sentences(data_file)

    for sentence in sentences:
        temp_sentece = punctuation_without_apostrophe.sub(' ', sentence)
        raw_tokens = temp_sentece.split(' ')
        tokens = [START]
        for token in raw_tokens:
            if not token.strip():
                continue
            word = punctuation.sub(' ', token)
            splited = word.split(' ')
            if splited[0] != '':
                tokens.append(splited[0])
                continue

            tokens.append(splited[1])

        predicted_tags = get_tags(tokens, vocabulary, tag_transition_prob, word_tag_prob)

        for i in range(len(tokens)):
            if tokens[i] == START:
                continue

            token_lemma = '_'
            if tokens[i] in vocabulary:
                token_lemma = vocabulary.get(tokens[i])

            output_text.append(tokens[i] + TAG_SEPARATOR + predicted_tags[i] + TAG_SEPARATOR + token_lemma)
        output_text.append("\n")

    file_util.write_array(output_file, output_text)


def get_word_tag_prob(word_tag_probs, tag, token):
    if token in word_tag_probs:
        if tag in word_tag_probs[token]:
            return word_tag_probs[token][tag]
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


def get_tags(tokens, vocabulary: dict, tag_transition_probs, word_tag_probs):
    viterbi = [0 for x in range(len(tokens))]

    postags = ['_' for x in range(len(tokens))]

    # Instantiation
    for tag in tag_transition_probs:
        if tag == START:
            continue

        if tokens[0] in vocabulary:
            token_lemma = vocabulary.get(tokens[0])
        else:
            token_lemma = tokens[0]

        posProb = get_safe_transition_prob(tag_transition_probs, START, tag) * get_word_tag_prob(word_tag_probs, tag,
                                                                                                 token_lemma)
        if posProb > viterbi[0]:
            viterbi[0] = posProb
            postags[0] = tag
    # Recursion
    for i in range(1, len(tokens)):
        posProb = 0
        if tokens[0] in vocabulary:
            token_lemma = vocabulary.get(tokens[i])
        else:
            token_lemma = tokens[i]
        for tag in tag_transition_probs:
            if tag == START:
                continue

            posProb = viterbi[i - 1] * get_safe_transition_prob(tag_transition_probs, postags[i - 1],
                                                                tag) * get_word_tag_prob(word_tag_probs,
                                                                                         tag,
                                                                                         token_lemma)
            if posProb > viterbi[i]:
                viterbi[i] = posProb
                postags[i] = tag

    return postags
