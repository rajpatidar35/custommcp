import sqlite3

# Define the SQL command to create the table
create_table_query = '''
CREATE TABLE IF NOT EXISTS SessionStore (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT NOT NULL,
    agent_id TEXT,
    session_id TEXT
);
''' # The IF NOT EXISTS clause prevents errors if the table already exists

# Use a context manager to handle the connection automatically
try:
    with sqlite3.connect('session.db') as connection:
        cursor = connection.cursor() # Create a cursor object

        # Execute the SQL command
        cursor.execute(create_table_query)

        # Commit the changes (this is done automatically when using 'with' but good practice to be explicit for other operations)
        connection.commit()

        print("Table 'SessionStore' created successfully!")

except sqlite3.Error as e:
    print(f"An error occurred: {e}")

# The connection is automatically closed when exiting the 'with' block
