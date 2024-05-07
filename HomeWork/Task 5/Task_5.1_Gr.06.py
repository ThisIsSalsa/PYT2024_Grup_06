import socket

# Prompt the user to input a URL
url = input("Enter the URL: ")

try:
    # Split the URL into its component parts
    parts = url.split("/")
    host = parts[2]

    # Create a socket connection to the host
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, 80))

    # GET request to retrieve the URL
    request = f"GET {url} HTTP/1.1\r\nHost: {host}\r\n\r\n"
    sock.sendall(request.encode())

    # Receive and count the characters in the response
    characters = 0
    while True:
        data = sock.recv(1024)
        if not data:
            break
        characters += len(data)
        if characters > 1700: #If bigger than 1700
            print(f"\nStopping display at 1700 characters\n")
            break
        print(data.decode(), end="")

except Exception as e:
    # Handle any exceptions that occur during execution
    print(f"Error: {e}")

finally:
    # Close
    sock.close()
