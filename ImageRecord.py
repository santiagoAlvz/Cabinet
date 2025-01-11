import hashlib
import sqlite3
import os

db_file = "Cabinet.db"
conn = None
cur = None

def connect(destination_dir):
    # If the database file doesn't exist (first run)
    if(not os.path.isfile(f"{destination_dir}/{db_file}")):
        create_database(destination_dir)

    conn = sqlite3.connect(f"{destination_dir}/{db_file}")

def create_database(destination_dir):
    conn = sqlite3.connect(f"{destination_dir}/{db_file}")
    cur = conn.cursor()

    cur.execute('''CREATE TABLE Execution(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATETIME,
        copied INTEGER
    )''')

    cur.execute('''CREATE TABLE Image(
        hash BINARY(32) PRIMARY KEY,
        fileName VARCHAR(64),
        executionId INTEGER,
        FOREIGN KEY (executionId) REFERENCES Execution(id)
    )''')

    cur.execute('''INSERT INTO Execution(date, copied)
                   VALUES(CURRENT_TIMESTAMP, 0)''')

    cur.execute(f'''INSERT INTO Image(hash, fileName, executionId)
                   VALUES('{hashlib.sha256(b'Juan').hexdigest()}',
                          'Juan',
                          {cur.lastrowid})''')

    conn.commit()
    conn.close()

def get_hash(image_path):
    with open(image_path, "rb") as f:
        hash = hashlib.sha256(f.read()).hexdigest()
    return hash