import hashlib
import sqlite3
import os

db_file = "Cabinet.db"
conn = None
cur = None
image_dir = None
destination_dir = None
current_execution_id = None

def connect(images, destination):
    global image_dir, destination_dir, conn, cur, current_execution_id

    image_dir = images
    destination_dir = destination

    # If the database file doesn't exist (first run)
    if(not os.path.isfile(f"{destination_dir}/{db_file}")):
        create_database()

    conn = sqlite3.connect(f"{destination_dir}/{db_file}")
    cur = conn.cursor()

    cur.execute('''INSERT INTO Execution(date, copied)
                   VALUES(CURRENT_TIMESTAMP, 0)''')

    current_execution_id = cur.lastrowid

def create_database():
    print(destination_dir)
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

    conn.commit()
    conn.close()

def verify(file):
    # Check if file with the same name exists
    cur.execute(f'''SELECT EXISTS (SELECT 1 FROM Image WHERE fileName = '{file}' LIMIT 1);''')
    
    if cur.fetchone()[0] == 1:
        return False
    else:
        return add_to_db(file)

def add_to_db(file):

    try:
        cur.execute(f'''INSERT INTO Image(hash, fileName, executionId)
                    VALUES('{get_image_hash(file)}',
                            '{file}',
                            {current_execution_id})''')
    except:
        print(f"- An image identical to {file} already exists in the destination!")
        return False

    conn.commit()
    return True

def get_image_hash(file):
    with open(image_dir + '/' + file, "rb") as f:
        hash = hashlib.sha256(f.read()).hexdigest()
    return hash

def close(copied_files):
    cur.execute(f'''UPDATE  Execution
                    SET copied = {copied_files}
                    WHERE id = {current_execution_id}''')
    conn.commit()
    conn.close()