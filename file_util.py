import json


def write_dic(filename, tokens, f_encoding='UTF-8'):
    with open(filename, 'w', encoding=f_encoding) as file:
        try:
            json.dump(tokens, file, ensure_ascii=True)
        except:
            print("Error writing +" + "=" * 25)
            print(tokens)

            # with open(filename, 'wb') as handle:
            #    pickle.dump(tokens, handle)


def read_dic(filename, f_encoding='UTF-8'):
    with open(filename, 'r', encoding=f_encoding) as file:
        return json.load(file)

        # with open(filename, 'rb') as handle:
        #    return pickle.load(handle)


def read_line_list(filename, f_encoding='UTF-8'):
    with open(filename, 'r', encoding=f_encoding) as file:
        return file.read().splitlines()


def write_csv(filename, data):
    with open(filename + ".csv", 'w') as of:
        for row in data:
            of.write(row + ";")
            of.write(str(data[row]))
            of.write("\n")


def write_array(output_file, text_array, f_encoding='UTF-8'):
    with open(output_file, 'w', encoding=f_encoding) as file:
        for item in text_array:
            file.write(item)
            if item != '\n':
                file.write('\n')
