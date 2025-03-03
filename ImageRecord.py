import hashlib
import sqlite3
import os

db_file = "Cabinet.db"
conn = None
cur = None
image_dir = None
destination_dir = None
current_execution_id = None
transaction_count = 0

# Tries to connect with SQLite database on the destination directory
def connect(images, destination):
    global image_dir, destination_dir, conn, cur, current_execution_id

    image_dir = images
    destination_dir = destination

    # If the database file doesn't exist (first run), create its
    if(not os.path.isfile(f"{destination_dir}/{db_file}")):
        create_database()

    conn = sqlite3.connect(f"{destination_dir}/{db_file}")
    cur = conn.cursor()

    cur.execute('''INSERT INTO Execution(date)
                   VALUES(CURRENT_TIMESTAMP)''')

    current_execution_id = cur.lastrowid

# Create a SQLite database for storing image information for subsequent runs
def create_database():
    print(destination_dir)
    conn = sqlite3.connect(f"{destination_dir}/{db_file}")
    cur = conn.cursor()

    cur.execute('''CREATE TABLE Execution(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATETIME
    )''')

    cur.execute('''CREATE TABLE File(
        hash BINARY(32) PRIMARY KEY,
        fileName VARCHAR(64),
        executionId INTEGER,
        FOREIGN KEY (executionId) REFERENCES Execution(id)
    )''')

    conn.commit()
    conn.close()

# Returns whether the file should be copied (it doesn't exist already in the destination)
def verify(file):
    # Check if file with the same name exists
    cur.execute(f'''SELECT EXISTS (SELECT 1 FROM File WHERE fileName = '{file}' LIMIT 1);''')
    
    if cur.fetchone()[0] == 1:
        return False
    else:
        return add_to_db(file)

# Add a new file record to the database
def add_to_db(file):
    global transaction_count

    try:
        cur.execute(f'''INSERT INTO File(hash, fileName, executionId)
                    VALUES('{get_image_hash(file)}',
                            '{file}',
                            {current_execution_id})''')
    except:
        print(f"- An image identical to {file} already exists in the destination!")
        return False

    transaction_count += 1

    if transaction_count % 20 == 0:
        print(transaction_count)
        conn.commit()

    return True

# Get the SHA256 hash from the file, useful for identifying if two
# images with different names are actually duplicates
def get_image_hash(file):
    with open(image_dir + '/' + file, "rb") as f:
        hash = hashlib.sha256(f.read()).hexdigest()
    return hash

# Commit pending changes and close the database
def close():
    conn.commit()
    conn.close()