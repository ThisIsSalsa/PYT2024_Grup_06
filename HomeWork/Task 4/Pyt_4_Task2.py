filename = input("Enter the file name: ")

try:
    file_handle = open(filename)
except:
    print("File cant  be opened:", filename)
    exit()

domain_dict = {}

for line in file_handle:
    if line.startswith("From "):
        words = line.split()
        email = words[1]
        domain = email.split('@')[1]
        domain_dict[domain] = domain_dict.get(domain, 0) + 1

sorted_domains = sorted(domain_dict.items())

for domain, count in sorted_domains:
    print(f"{domain:25s}: {count} {'*' * count}")
