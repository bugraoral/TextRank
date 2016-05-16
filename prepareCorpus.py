filePath = 'METUSABANCI_treebank.conll'
writePath = 'corpus.sdx'
with open(writePath,'w') as w:
    with open(filePath) as f:
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0:
                w.writelines('\n')
            else:
                tmp = line.split()
                word = tmp[1]
                if word != '_':
                    tag = tmp[3]
                    w.writelines(word.lower()+'|'+tag+'\n')
