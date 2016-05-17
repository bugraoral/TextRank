import nltk
import string
import itertools
import re
from pos_tagger import tag
import matplotlib.pyplot as plt

filePath = 'news/siyaset/441.txt'


def extract_candidate_words(text, good_tags=set(['Adj', 'Noun', 'Noun_Nom', 'Verb'])):
    stop_words = set(nltk.corpus.stopwords.words('turkish'))


    tagged_words = itertools.chain.from_iterable((tag(removePunc(sent).strip())
                                                for sent in nltk.sent_tokenize(text)))

    candidates = [word.lower() for word, tag in tagged_words
                  if tag in good_tags and word.lower() not in stop_words
                  and (len(word) > 2)]

    return candidates

def removePunc(text):
    punct = set(string.punctuation)
    noPuncText = ''
    for ch in text:
        if ch in punct:
            noPuncText += ' '
        else:
            noPuncText += ch
    return noPuncText

def score_keyphrases_by_textrank(text, n_keywords=0.05):
    from itertools import takewhile, tee
    import networkx, nltk

    stop_words = set(nltk.corpus.stopwords.words('turkish'))

    # tokenize for all words, and extract *candidate* words
    words = [word.lower()
             for sent in nltk.sent_tokenize(text)
             for word in nltk.word_tokenize(removePunc(sent).strip())
             if len(word) > 2 and word.lower() not in stop_words]

    candidates = extract_candidate_words(text)
    # build graph, each node is a unique candidate
    graph = networkx.Graph()
    graph.add_nodes_from(set(candidates))
    # iterate over word-pairs, add unweighted edges into graph

    def pairwise(iterable):
        """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)
    for w1, w2 in pairwise(candidates):
        if w2:
            graph.add_edge(*sorted([w1, w2]))
    # score nodes using default pagerank algorithm, sort by score, keep top n_keywords
    ranks = networkx.pagerank(graph)

    if 0 < n_keywords < 1:
        n_keywords = int(round(len(candidates) * n_keywords))
    word_ranks = {word_rank[0]: word_rank[1]
                  for word_rank in sorted(ranks.items(), key=lambda x: x[1], reverse=True)[:n_keywords]}
    keywords = set(word_ranks.keys())
    # merge keywords into keyphrases
    keyphrases = {}
    j = 0
    for i, word in enumerate(words):
        if i < j:
            continue
        if word in keywords:
            kp_words = list(takewhile(lambda x: x in keywords, words[i:i+10]))
            indexL = words[i:i+10].index(kp_words[0])
            indexR = words[i:i+10][::-1].index(kp_words[-1])
            test_words = words[indexL:indexR+1]
            avg_pagerank = sum(word_ranks[w] for w in kp_words) / float(len(kp_words))
            keyphrases[' '.join(test_words)] = avg_pagerank
            # counter as hackish way to ensure merged keyphrases are non-overlapping
            j = i + len(test_words)

    for item in candidates:
        if item not in keywords and item in graph:
            graph.remove_node(item)

    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)

    sp = networkx.spring_layout(graph)
    networkx.draw_networkx_nodes(graph,sp)
    networkx.draw_networkx_edges(graph,sp)
    networkx.draw_networkx_labels(graph,sp)

    plt.show()

    return sorted(keyphrases.items(), key=lambda x: x[1], reverse=True)

with open(filePath) as f:
    text = f.read()

keywords = score_keyphrases_by_textrank(text)

for keyword,score in keywords:
    print(keyword,score)