import sqlite3
import re

# Function to extract domain from an email address
def extract_domain(email):
    return email.split('@')[1]

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('email_spam.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS email_address (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    weekday TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS domain_name (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain TEXT NOT NULL UNIQUE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS spam_confidence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email_id INTEGER NOT NULL,
    confidence_level REAL,
    FOREIGN KEY (email_id) REFERENCES email_address(id)
)
''')

conn.commit()

# Read the mbox file
with open('mbox-short.txt', 'r') as file:
    lines = file.readlines()

# Regular expressions for matching email addresses and spam confidence levels
email_pattern = re.compile(r'^From (\S+@\S+)')
spam_confidence_pattern = re.compile(r'^X-DSPAM-Confidence: ([0-9.]+)')

email = None
weekday = None
spam_confidence = None

for line in lines:
    # Match email addresses
    email_match = email_pattern.match(line)
    if email_match:
        email = email_match.group(1)
        
        # Extract weekday if available
        parts = line.split()
        if len(parts) >= 3:
            weekday = parts[2]
        
        # Insert email and weekday into the email_address table if not exists
        cursor.execute('INSERT OR IGNORE INTO email_address (email, weekday) VALUES (?, ?)', (email, weekday))
        cursor.execute('SELECT id FROM email_address WHERE email = ?', (email,))
        email_id = cursor.fetchone()[0]
        
        # Extract domain and insert into the domain_name table if not exists
        domain = extract_domain(email)
        cursor.execute('INSERT OR IGNORE INTO domain_name (domain) VALUES (?)', (domain,))
    
    # Match spam confidence levels
    spam_confidence_match = spam_confidence_pattern.match(line)
    if spam_confidence_match and email:
        spam_confidence = float(spam_confidence_match.group(1))
        
        # Insert spam confidence into the spam_confidence table
        cursor.execute('INSERT INTO spam_confidence (email_id, confidence_level) VALUES (?, ?)', (email_id, spam_confidence))
        email = None  # Reset email to avoid duplicate entries in the next iteration

conn.commit()

# Fetch and display unique domains
cursor.execute('SELECT DISTINCT domain FROM domain_name')
unique_domains = cursor.fetchall()

print("List of unique domains:")
for domain in unique_domains:
    print(domain[0])

# Get user input for domain selection
chosen_domain = input("\nEnter a domain name from the list above: ").strip()

# Query the database for emails from the chosen domain on Fri and Sat, ordered by spam confidence level
query = '''
SELECT DISTINCT email_address.weekday, domain_name.domain, email_address.email, spam_confidence.confidence_level
FROM email_address
JOIN domain_name ON email_address.email LIKE '%' || domain_name.domain
JOIN spam_confidence ON email_address.id = spam_confidence.email_id
WHERE domain_name.domain = ?
AND email_address.weekday IN ('Fri', 'Sat')
ORDER BY spam_confidence.confidence_level
'''

cursor.execute(query, (chosen_domain,))
results = cursor.fetchall()

# Display the results
print("\nResults for emails from domain '{}':".format(chosen_domain))
for row in results:
    print("Weekday: {}, Domain: {}, Email: {}, SPAM Confidence: {}".format(row[0], row[1], row[2], row[3]))

# Close the database connection
conn.close()