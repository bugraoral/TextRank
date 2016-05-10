import file_util
import hmm_article_tagger
import os
import shutil
import conllxi_reader

INPUT_DIR = "news"
OUTPUT_DIR = "news_postagged"

sentences = conllxi_reader.read_conllxi("turkish_metu_sabanci_train.conll")


def build_vocabulary(sentences):
    '''
    Parses given sentences to find word-lemma relations to build a vocabulary
    :param sentences: in form of conll
    :return: dict key - value : word - lemma
    '''
    vocabulary = dict()
    for sentence in sentences:
        valid_tokens = sentence.get_valid_tokens()

        for word in valid_tokens:
            vocabulary[word.get_form()] = word.get_representation()

    return vocabulary


vocabulary = build_vocabulary(sentences)
word_tag_prob = file_util.read_dic(".word_prob")
tag_transition_prob = file_util.read_dic(".transition_prob")

if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)

os.mkdir(OUTPUT_DIR)

categories = os.listdir("news")
# categories = [categories[0]]
for category in categories:

    category_path = os.path.join(INPUT_DIR, category)
    output_category_path = os.path.join(OUTPUT_DIR, category)

    news = os.listdir(category_path)
    os.mkdir(output_category_path)

    # news = [news[0]]
    for article in news:
        article_path = os.path.join(category_path, article)
        output_article_path = os.path.join(output_category_path, article)
        hmm_article_tagger.tag(article_path, output_article_path, vocabulary, tag_transition_prob, word_tag_prob)
        print(article_path + " tagged.")
