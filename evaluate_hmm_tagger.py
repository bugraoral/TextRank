import argparse

import conllxi_reader
import file_util
from pandas import DataFrame

SEPARATOR = '|'
TAG_TYPE = None


def evaluate(output, gold):
    assert output
    assert gold

    output_lines = file_util.read_line_list(output)
    gold_sentences = conllxi_reader.read_conllxi(gold)

    gold_lines = []

    for sentence in gold_sentences:
        for token in sentence.get_valid_tokens():
            gold_lines.append(token.get_form() + SEPARATOR + token.get_data()[TAG_TYPE])
        gold_lines.append("\n")

    confusion = dict(dict())

    error_counter = 0
    total_counter = 0

    for i in range(len(output_lines)):
        if output_lines[i] == "" or output_lines[i] == "\n":
            continue

        total_counter += 1
        predicted_row = output_lines[i].split(SEPARATOR)
        gold_row = gold_lines[i].split(SEPARATOR)

        if not (predicted_row[0] == gold_row[0]):
            print(predicted_row[0] + " is not " + gold_row[0])
            continue

        if gold_row[1] not in confusion:
            confusion[gold_row[1]] = dict()

        if predicted_row[1] != gold_row[1]:
            error_counter += 1
            if predicted_row[1] not in confusion[gold_row[1]]:
                confusion[gold_row[1]][predicted_row[1]] = 1
            else:
                confusion[gold_row[1]][predicted_row[1]] += 1

    print("===" * 50)
    print("Overall result %" + str(((total_counter - error_counter) / total_counter) * 100))
    print("===" * 50)
    df = DataFrame(confusion).T.fillna(0)
    print(df.to_string())
    print("===" * 50)

    df.to_csv(output + "_confusion.csv", encoding='utf-8')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('output', help='Path of tagged output file')
    parser.add_argument('gold', help='Path of gold standard file')
    parser.add_argument('--postag', action="store_true",
                        help='uses cpostag by default input --postag to switcg')
    parser.add_argument('--cpostag', action="store_true",
                        help='uses cpostag by default input --postag to switcg')

    opts = parser.parse_args()

    if opts.postag:
        TAG_TYPE = 4
    else:
        TAG_TYPE = 3

    evaluate(opts.output, opts.gold)
