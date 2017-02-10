import sqlite3

with sqlite3.connect('test.db') as conn:
    c = conn.cursor()

    with open("test_query.out", 'w') as f:
        for row in c.execute('''SELECT word, COUNT(*) as count FROM words \
            GROUP BY word ORDER BY count DESC'''):
            for e in row:
                f.write(str(e) + " ")
            f.write("\n")
