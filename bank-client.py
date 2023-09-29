import socket
import sys


def run_bank_client():
    """ Runs the client program
    
    """
    try:
        host = socket.gethostbyname(socket.gethostname())
        port = 65432
    except socket.gaierror:
        print('Could not get hostname...Ending client.')
        sys.exit()

    # Creates a socket object
    print(f"Client is starting - connectiong to server at IP, {host}, and port, {port}")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:

            # Establishes a connection with server
            client_sock.connect((host, port))
            print(f"Connected to the server.")

            intro = client_sock.recv(1024)
            intro = intro.decode("utf-8")
            print(intro)

            while True:
                # Asks user to input its request to be sent over to the server. 
                
                request = input("Enter request: ")
                print("Sending request...") 
                client_sock.send(request.encode("utf-8")[:1024])

                # Receives a response from the server.
                response = client_sock.recv(1024)
                response = response.decode("utf-8")

                # If the server sends "Close", the loop is broken and the socket is closed.
                if response == "Closed":
                    break

                print(f"Received: {response}")

            # Close client_sock socket - the connection the server
            client_sock.close()
            print("Connection to server closed.")
    except socket.error:
            print("Failed to create socket:(")
            sys.exit()


run_bank_client()