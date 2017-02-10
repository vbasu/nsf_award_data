import os
import nltk
import sqlite3
import re

def main():
    with sqlite3.connect('abstract_titles.db') as conn:
        conn.text_factory = str
        cur = conn.cursor()
        cur.execute('''DROP TABLE IF EXISTS words''')
        cur.execute('''CREATE TABLE words
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                year INTEGER,
                word TEXT)''')
        count = 0
        broken = 0
        for subdir, dirs, files in os.walk(os.getcwd()):
            m = re.search('[0-9]{4}', subdir)
            if not m:
                continue
            else:
                year = m.group(0)
                #print "YEAR:", year
            for f in files:
                #print subdir, dirs, files
                #print os.path.join(subdir, file)
                filepath = subdir + os.sep + f

                if filepath.endswith(".txt"):
                    with open(filepath, 'r') as g:
                        a = g.readline()
                        b = a[:14]
                        if not b == 'Title       : ':
                            broken += 1
                            print "BROKEN FORMAT TITLE:", a
                        c = a[14:]
                        relevant_words = []
                        #words = map(lambda x: x.lower(), c.split())
                        text_list = nltk.word_tokenize(c)
                        tagged_text = nltk.pos_tag(text_list)

                        for word, pos in tagged_text:
                            if accepted_part_of_speech(pos) and not word in {'(',')'}:
                                #nltk pos tagger somtimes includes parens
                                relevant_words.append(word)
                        count += 1
                        for w in relevant_words: #some odd chars exist
                            if w.isalnum():
                                entry = (year, w.lower())
                                cur.execute('INSERT INTO words(year, word) \
                                        VALUES (?, ?)', entry)

        print "Total files considered: %d" % count
        print "Exceptions to the rule: %d" % broken

def accepted_part_of_speech(pos):
    return pos in {'JJ', 'JJR', 'JJS', 'NN', 'NNS', 'NNP', 'NNPS'}

if __name__ == "__main__":
    main()
