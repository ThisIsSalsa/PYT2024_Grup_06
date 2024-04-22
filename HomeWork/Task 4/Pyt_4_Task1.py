fname = input("Enter a file name: ")
try:
    fhand = open(fname)
except:
    print("File cannot be opened:", fname)
    exit()
senders = []

for line in fhand:
    if line.startswith("From "):
        senders.append(line.split()[1])

for sender in sorted(senders):
    print(sender)

print("There were", len(senders), "lines in the file with From as the first word")