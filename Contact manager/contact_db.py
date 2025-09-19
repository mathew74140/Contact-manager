import sqlite3

class ContactDB:
    def __init__(self, db_path='mycontacts.db'):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fname TEXT,
                lname TEXT,
                address TEXT,
                phone TEXT
            )
        ''')
        self.conn.commit()

    def insert(self, fname, lname, address, phone):
        self.cur.execute('INSERT INTO contacts (fname, lname, address, phone) VALUES (?, ?, ?, ?)',
                         (fname, lname, address, phone))
        self.conn.commit()

    def select(self):
        self.cur.execute('SELECT * FROM contacts')
        return self.cur.fetchall()

    def delete(self, id):
        self.cur.execute('DELETE FROM contacts WHERE id = ?', (id,))
        self.conn.commit()

    def update(self, id, fname, lname, address, phone):
        self.cur.execute('''
            UPDATE contacts SET fname = ?, lname = ?, address = ?, phone = ? WHERE id = ?
        ''', (fname, lname, address, phone, id))
        self.conn.commit()
cdb = ContactDB('d:/mycontacts.db')