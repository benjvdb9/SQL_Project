import sqlite3

def importdb(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for table in c.fetchall():
        yield list(c.execute("SELECT * from ?;", (table[0],)))


if '__name__' == '__main__':
    print('test')
    importdb('sqlalchemy_example.db')
