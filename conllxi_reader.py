import file_util
import sentence


def read_conllxi(path):
    lines = file_util.read_line_list(path, f_encoding='UTF-8')
    sentences = []
    temp = []
    for line in lines:
        if line == "":
            sentences.append(sentence.Sentence(temp))
            temp = []
        else:
            temp.append(line)

    if len(temp) != 0:
        sentences.append(sentence.Sentence(temp))

    return sentences

# sentences = read_conllxi("metu_sabanci_cmpe_561_v2/train/turkish_metu_sabanci_train.conll")

# for sentence in sentences:
#    print(sentence.get_human_sentence())
