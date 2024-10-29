# backend.py
import sqlite3

# Connect to or create a SQLite database
conn = sqlite3.connect("phone_numbers.db", check_same_thread=False)
cursor = conn.cursor()

# Drop the table if it exists to avoid schema conflicts, then recreate it
cursor.execute("DROP TABLE IF EXISTS PhoneNumbers")
conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS PhoneNumbers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone_number TEXT UNIQUE,
    Client_code TEXT UNIQUE
)
""")
conn.commit()

# Function to add a phone number with an additional number
def add_phone_number(phone_number, Client_code):
    # Validate the phone number length
    if len(phone_number) != 10 or not phone_number.isdigit():
        return "Invalid phone number. It must be exactly 10 digits."
    
    # Validate the additional number length
    if len(Client_code) not in [5, 6] or not Client_code.isdigit():
        return "Invalid Client_code. It must be either 5 or 6 digits."
    
    try:
        cursor.execute("INSERT INTO PhoneNumbers (phone_number, Client_code) VALUES (?, ?)", 
                       (phone_number, Client_code))
        conn.commit()
        return f"Phone number {phone_number} with Client_code {Client_code} added successfully."
    except sqlite3.IntegrityError:
        return f"Phone number {phone_number} or Client_code {Client_code} already exists in the database."

# Function to list all phone numbers with their additional numbers
def list_phone_numbers():
    cursor.execute("SELECT phone_number, Client_code FROM PhoneNumbers")
    numbers = cursor.fetchall()
    if not numbers:
        return "No phone numbers stored."
    return "\n".join([f"Phone Number: {number[0]}, Client_code: {number[1]}" for number in numbers])
