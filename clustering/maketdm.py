import TdMat
from nltk.corpus import brown

for f in brown.fileids():
    docs = TdMat.process_sample(f)
    print f
    for doc in  docs:
        TdMat.tdm.add_doc(doc)

import re
class_num = []
for f in brown.fileids():
    docs = TdMat.process_sample(f)
    ch = re.findall(r'c([a-r])\d\d',f)[0]
    for doc in  docs:
        class_num.append(ord(ch) - 96)

