import sqlite3
import matplotlib.pyplot as plt

def main(s):
    with sqlite3.connect('abstract_titles.db') as conn:
        c = conn.cursor()
        years = []
        freq = []
        for row in c.execute('''SELECT year, COUNT(*) as count \
                FROM words \
                WHERE word = "undergraduate" \
                GROUP BY year;
                '''
                ):
            i = 0
            while i < len(row):
                years.append(row[i])
                freq.append(row[i+1])
                i += 2

    plt.title("Frequency of \"%s\" from 1990-2002" % s)
    plt.plot(years[:-1], freq[:-1])
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main("undergraduate")
