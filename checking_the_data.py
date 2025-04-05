import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('recruitment.db')
cursor = conn.cursor()

# Query data from a table
#cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
cursor.execute("SELECT * FROM match_scores;")

# Fetch and print all rows
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()
