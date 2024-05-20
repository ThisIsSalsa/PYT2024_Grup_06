import sqlite3
import re

def extract_domain(email):
    return email.split('@')[1]

conn = sqlite3.connect('email_spam.db')
cursor = conn.cursor()

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

with open('mbox-short.txt', 'r') as file:
    lines = file.readlines()

email_pattern = re.compile(r'^From (\S+@\S+)')
spam_confidence_pattern = re.compile(r'^X-DSPAM-Confidence: ([0-9.]+)')

email = None
weekday = None
spam_confidence = None


for line in lines:

    email_match = email_pattern.match(line)
    if email_match:
        email = email_match.group(1)
 
        parts = line.split()
        if len(parts) >= 3:
            weekday = parts[2]
   
        cursor.execute('INSERT OR IGNORE INTO email_address (email, weekday) VALUES (?, ?)', (email, weekday))
        cursor.execute('SELECT id FROM email_address WHERE email = ?', (email,))
        email_id = cursor.fetchone()[0]
   
        domain = extract_domain(email)
        cursor.execute('INSERT OR IGNORE INTO domain_name (domain) VALUES (?)', (domain,))

    spam_confidence_match = spam_confidence_pattern.match(line)
    if spam_confidence_match and email:
        spam_confidence = float(spam_confidence_match.group(1))

        cursor.execute('INSERT INTO spam_confidence (email_id, confidence_level) VALUES (?, ?)', (email_id, spam_confidence))

conn.commit()

cursor.execute('SELECT DISTINCT domain FROM domain_name')
unique_domains = cursor.fetchall()

print("List of unique domains:")
for domain in unique_domains:
    print(domain[0])

chosen_domain = input("\nEnter a domain name from the list above: ").strip()

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

displayed_confidences = set()

print("\nEmails received from domain '{}' on Fridays and Saturdays:".format(chosen_domain))
print("{:<10} {:<20} {:<30} {:<10}".format('Weekday', 'Domain', 'Email', 'Spam Confidence'))
print('-' * 70)

for row in results:
    if row[3] not in displayed_confidences:
        print("{:<10} {:<20} {:<30} {:<10}".format(row[0], row[1], row[2], row[3]))
        displayed_confidences.add(row[3])
 
        if len(displayed_confidences) >= 10:
            break

conn.close()