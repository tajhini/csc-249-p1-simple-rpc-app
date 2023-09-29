import socket
import sys

account_balance = 1000

# This function anaylyses the request to ensure that it meets the requirements.
def analyse_request(request):
    """ Analyses the request made by the client by putting it in a format that
        can be understood by the withdraw and deposit functions.

        :param request: (String): The request made by the client.
        :return response: A message of the new account balance.
    """
    
    split_req = request.split(" ")
    
    if (len(split_req) == 2 and (split_req[1].isdigit() == True)):
        if (split_req[0] == "Deposit" ):
            response =  deposit(int(split_req[1]))
        
        elif (split_req[0] == "Withdraw"):
            response =  withdraw( int(split_req[1]))
        else:
            response = ("This is not a recognised request. Please reenter your request in the specified format.")
        
    else:
         response = ("This is not a recognised request. Please reenter your request in the specified format.")
    return response

# This function adds money to the user's account.
def deposit(money):
    """ Adds money to the user's account.

    :param money: (int): The amount of money to be deposited.
    :return message: A message with the new account balance.

    >>> deposit(1200)
    3200
    """

    global account_balance
    account_balance = account_balance + money
    message = (f"Your new balance is ${account_balance}.")
    return message
    
# This function subtracts money from the user's account.
def withdraw(money):
    """ Subtracts money from the user's account.

    :param money: (int): The amount of money to be withdrawn.
    :return message: A message with the new account balance.

    >>> withdraw(100)
    900
    """

    global account_balance
    account_balance = account_balance - money
    if account_balance < 0:
        message =  ("Insufficient Funds.")
        account_balance = account_balance + money
    else:
        message = (f"Your new balance is ${account_balance}.")
    return message


def run_bank_server():
    """ Runs the server.
    """
    # Gets the ip address of the local machine.
    try:
        host = socket.gethostbyname(socket.gethostname())
        port = 65432
    except socket.gaierror:
        print('Could not get hostname...Ending server.')
        sys.exit()
        
    # Creates a socket
    print(f"Server is starting - listening for connections at IP", {host}, "and port", {port})
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:


            # Binds the  socket to the specified address and port above
            serv_sock.bind((host, port))

            # Listening for incoming connections
            serv_sock.listen()
            print(f"Listening on {host}:{port}")

            # Accepting any incoming connections
            client_conn, client_addy = serv_sock.accept()
            print(f"Accepted connection from {client_conn} at {client_addy}.")

            # Sends instructions to the client
            instructions = "This server depsoits and withdraws money. \nTo do that, enter 'Deposit [amount]' or 'Withdraw [amount]'. \nEnter 'Close' to close sever. \n"
            client_conn.send(instructions.encode("utf-8"))

            while True:

                request = client_conn.recv(1024)
                request = request.decode("utf-8") # convert bytes to string
                analysed_req = analyse_request(request)
                
                # Connection is closed if server recieves "Close".
                if request == "Close":
                    # Sends a response to the client that the server has closed.
                    client_conn.send("Closed".encode("utf-8"))
                    break

                # Continues with operation as usual
                print(f"Received your request to: {request}")

                response = analysed_req.encode("utf-8") # convert string to bytes
                # convert and send accept response to the client

                client_conn.send(response)
                print("Response has been sent. Waiting...")

            # Closes connection socket with the client
            client_conn.close()
            print("Connection to client has been closed.")
            #Closes server socket
            serv_sock.close()
    except:
        print('Failed to create socket:(')
        sys.exit()


run_bank_server()

