'''
Parse the nsf award files

Fields:
    Title
    Type
    NSF Org
    Latest Amendment Date
    File
    Award Number
    Award Instr.
    Program Manager
    Start Date
    Expiration Date
    Expected Total Amount
    Investigator
    Sponsor
    NSF Program
    Fld Application
    Program Ref
    Abstract
'''

import os
import nltk
import sqlite3
import re

def main():
    with sqlite3.connect('abstracts.db') as conn:
        conn.text_factory = str
        cur = conn.cursor()
        cur.execute('''DROP TABLE IF EXISTS abstracts''')
        cur.execute('''CREATE TABLE abstracts
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    type TEXT,
                    nsf_org TEXT,
                    latest_amendment_date TEXT,
                    file TEXT,
                    award_number TEXT,
                    award_instr TEXT,
                    program_manager TEXT,
                    start_date TEXT,
                    expiration_date TEXT,
                    expected_total_amount TEXT,
                    investigator TEXT,
                    sponsor TEXT,
                    nsf_program TEXT,
                    field_application TEXT,
                    program_ref TEXT,
                    abstract TEXT)''')
        success = 0
        failed = 0
        for subdir, dirs, files in os.walk(os.getcwd()):
            m = re.search('[0-9]{4}', subdir)
            if not m:
                continue
            else:
                year = m.group(0)
            for f in files:
                filepath = subdir + os.sep + f

                if filepath.endswith(".txt"):
                    with open(filepath, 'r') as g:
                        text = g.read()
                    try:
                        info = parse(text)
                    except ValueError:
                        failed += 1
                        continue
                    entry = tuple(info)
                    cur.execute('''INSERT INTO
                            abstracts(title,
                            type,
                            nsf_org,
                            latest_amendment_date,
                            file,
                            award_number,
                            award_instr,
                            program_manager,
                            start_date,
                            expiration_date,
                            expected_total_amount,
                            investigator,
                            sponsor,
                            nsf_program,
                            field_application,
                            program_ref,
                            abstract)
                            VALUES
                            (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
                            , entry)
                    success += 1

    print "Files parsed: %d" % success 
    print "Files failed: %d" % failed

def parse(s):
    fields = []
    a, s = re.split('Title\s*: ', s)
    a, s = re.split('Type\s*: ', s)
    fields.append(clean(a))

    a, s = re.split('NSF Org\s*: ', s)
    fields.append(clean(a))

    a, s = re.split('Latest\s*Amendment\s*Date\s*: ', s)
    fields.append(clean(a))

    a, s = re.split('File\s*: ', s)
    fields.append(clean(a))

    a, s = re.split('Award Number\s*: ', s)
    fields.append(clean(a))

    a, s = re.split('Award Instr.\s*: ', s)
    fields.append(clean(a))

    a, s = re.split('Prgm Manager\s*: ', s)
    fields.append(clean(a))

    a, s = re.split('Start Date\s*: ', s)
    fields.append(clean(a))

    a, s = re.split('Expires\s*: ', s)
    fields.append(clean(a))

    a, s = re.split('Expected\s*Total\s*Amt.\s*: ', s)
    fields.append(clean(a))

    a, s = re.split('Investigator\s*: ', s)
    fields.append(clean(a))

    a, s = re.split('Sponsor\s*: ', s)
    fields.append(clean(a))

    a, s = re.split('NSF Program\s*: ', s)
    fields.append(clean(a))

    a, s = re.split('Fld Applictn\s*: ', s)
    fields.append(clean(a))

    a, s = re.split('Program Ref\s*: ', s)
    fields.append(clean(a))

    a, s = re.split('Abstract\s*:', s)
    fields.append(clean(a))

    fields.append(clean(s))

    return fields

def clean(s):
    s = s.strip()
    s = re.sub('\s+', ' ', s)
    return s

if __name__ == "__main__":
    main()
