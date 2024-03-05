import socket
import threading
import time
import csv
import requests
import webbrowser
def new():
    try:
        savdat=open("user_data.csv","w")
        savdat.close()
        savdat2=open("logs.csv","w")
        header=["USER-NAME","USER-ACTIVITY","CONNECTION-TIME","RESPONSE-MESSAGE","CONNECTION-STATUS","WEB-SECURITY-STATUS"]
        userdat=[header]
        writeup=csv.writer(savdat2)
        writeup.writerow(userdat)
        savdat2.close()
    except Exception as e:
        print("Error creating files:", e)

def signup():
    try:
        global acheck
        global a
        global b
        global c
        verifusernum=0
        print("\nDisclaimer -> please dont use the already taken usernames as it will lead to incorrect data or errors.\n")
        a=input("enter your username  ")
        b=input("enter your password  ")
        c=input("re-enter your password  ")
        savdat=open("user_data.csv","r")
        verifuserdoub=csv.reader(savdat)
        for x in verifuserdoub:
            if x[0]==a:
                verifusernum=verifusernum+1
                if verifusernum>=1:
                    print("sorry username already taken, please try some other username")
                    signup()
        pass_check()
    except Exception as e:
        print("Error during signup:", e)
        main_page()
def pass_check():
    try:
        global acheck
        global a
        global b
        global c
        if b!=c:
            while b!=c:
              print("the password re-entered does not match with original")
              b=input("enter your password  ")
              c=input("re-enter your password  ")
              if b==c:
                  break
        print("thank you for signing up with us",a)
        savdat=open("user_data.csv","a",newline="")
        userdat=[a,b]
        writeup=csv.writer(savdat)
        writeup.writerow(userdat)
        savdat.close()
        print("\nand just like that your account has been successfully created",a,"\n")
        acheck=a
        start_app()
    except Exception as e:
        print("Error during password checking:", e)
        pass_check()

def login():
    try:
        usercount=0
        global acheck
        acheck=input("enter your username  ")
        bcheck=input("enter your password  ")
        savdat=open("user_data.csv","r")
        verif1=csv.reader(savdat)
        for line in verif1:
            if line[0]==acheck and line[1]==bcheck:
                usercount=usercount+1
        if usercount==1:
                print("welcome back",acheck)
                start_app()
        else:
            print("\nERROR ! username or password is incorrect , please retype the username and password or create a new account")
            login1=input("enter r if you want to re-login, enter p if you want to signup  ")
            if login1=="r":
                login()
            if login1=="p":
                signup()
            else:
                print("please enetr a valid input.")
                sign_up()
        savdat.close()
    except Exception as e:
        print("Error during login:", e)
def display_user_activity():
    try:
        global acheck
        print("\nUser activity for user:", acheck)
        with open("logs.csv", "r") as logs_file:
            reader=csv.reader(logs_file)
            next(reader)
            for row in reader:
                if row and row[0] == acheck:
                    print("\nUser: {}".format(row[0]))
                    print("Activity: {}".format(row[1]))
                    print("Connection Time: {}".format(row[2]))
                    print("Response Message: {}".format(row[3]))
                    print("Connection Status: {}".format(row[4]))
                    print("Web Security Status: {}".format(row[5]))
    except Exception as e:
        print("Error displaying user activity:", e)
    start_app()
        
def get_local_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception as e:
        print("Error getting local IP:", e)
        return None

def send_message_tcp(host,port,message):
    try:
        client_tcp=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client_tcp.connect((host,port))
        print("\nSuccessfully connected to the TCP server")
        client_tcp.sendall(message.encode())
        client_tcp.close()
    except Exception as e:
        print("Error in TCP client:", e)

def receive_message_tcp(host, port):
    try:
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind((host,port))
        server.listen(1)
        print("\nTCP server is listening on {}:{}".format(host, port))
        client_socket, client_address = server.accept()
        data = client_socket.recv(1024)
        print("Received TCP message from {}:{}".format(client_address, data.decode("utf-8")))
        client_socket.close()
    except Exception as e:
        print("Error in TCP server:",e)

def send_message_udp(host, port, message):
    try:
        client_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("\nSuccessfully connected to the UDP server")
        client_udp.sendto(message.encode(),(host, port))
        client_udp.close()
    except Exception as e:
        print("Error in UDP client:",e)

def receive_message_udp(host, port):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind((host, port))
        print("\nUDP server is listening on {}:{}".format(host, port))
        data, client_address = server.recvfrom(1024)
        print("Received UDP message from {}: {}".format(client_address,data.decode("utf-8")))
    except Exception as e:
        print("Error in UDP server:",e)

def web_connect(web_ip,web_port):
    try:
        global success_log
        global time_log
        global response_log
        start_time=time.time()
        server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.connect((web_ip,web_port))
        end_time=time.time()
        con_time=end_time-start_time
        print("\nSuccessfully connected to website at {}:{}".format(web_ip,web_port))
        print("Connection time:{:.2f}seconds".format(con_time))
        req="GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(web_ip)
        success_log="Successfully connected to website at {}:{}".format(web_ip,web_port)
        time_log="Connection time:{:.2f}seconds".format(con_time)
        server.sendall(req.encode())
        response=server.recv(4096)
        print("Received response from website:\n",response.decode())
        response_log="Received response from website:\n",response.decode()
        server.close()
    except Exception as e:
        print("Error in web connection:", e)
        success_log="Error in web connection:", e
        time_log="null"
        response_log="null"
        start_app()

def connection_check(web):
    try:
        global status_log
        socket.setdefaulttimeout(5)  
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((web,443))
        print(f"Connection to {web} is strong.")
        status_log=f"Connection to {web} is strong."
        check_website_security(web)
    except Exception as e:
         print(f"Failed to establish a connection to {web}. Error:", e, "Please check your internet connection once again.")
         status_log=f"Failed to establish a connection to {web}. Error:", e, "Please check your internet connection once again."
         start_app()
def check_website_security(web):
    try:
        global acheck
        global success_log
        global time_log
        global response_log
        global status_log
        url="https://"+web
        response=requests.get(url)
        print("SSL Certificate Validity:", response.ok)
        security_log="SSL Certificate Validity:", response.ok
        security_headers = response.headers
        print("HTTP Security Headers:")
        for header, value in security_headers.items():
            if header.lower().startswith('content-security-policy') or \
               header.lower().startswith('strict-transport-security') or \
               header.lower().startswith('x-content-type-options') or \
               header.lower().startswith('x-frame-options') or \
               header.lower().startswith('x-xss-protection'):
                print(header + ":", value)
    except Exception as e:
        print("Error checking website security:", e)
        security_log="Error checking website security:", e
    savdat=open("logs.csv","a",newline="")
    userdat=[acheck,success_log,time_log,response_log,status_log,security_log]
    writeup=csv.writer(savdat)
    writeup.writerow(userdat)
    savdat.close()
    option=input("\ndo you want to visit this site ? enter yes or no : ")
    if option=="yes":
        webbrowser.open(url)
    elif option=="no":
        print("\nalright then")
    else:
        start_app()
    start_app()
def start_app():
    try:
        host=get_local_ip()
        if host is None:
            print("Failed to retrieve local IP address.")
            return
        port_tcp=12345
        port_udp=54321
        con_type=input("\nEnter communication_tcp, communication_udp, advanced_website, simple_website, quick_select_sites based on what type of connection you want to utilize \nenter log_out if you want to quit\nenter display_user_history to see your history: ")
        if con_type=="communication_tcp":
            dest_ip=input("\nEnter the destination's IP address: ")
            sr=input("\nsend or recieve ? ")
            if sr=="send":
                sendmsg=str(input("\nenter your message : "))
                send_message_tcp(dest_ip,port_tcp,sendmsg)
            elif sr=="recieve":
                receive_message_tcp(host,port_tcp)
            else:
                print("\n please select a valid option .")
                start_app()
            start_app()
        elif con_type=="communication_udp":
            dest_ip=input("Enter the destination's IP address: ")
            src=input("\nsend or recieve ? ")
            if src=="send":
                sendumsg=str(input("\nenter your message : "))
                send_message_udp(dest_ip,port_udp,sendumsg)
            elif src=="recieve":
                receive_message_udp(host,port_udp)
            else:
                print("\n please select a valid option .")
                start_app()
            start_app()
        elif con_type=="advanced_website":
            web_ip=input("Enter website's IP address: ")
            web_port=int(input("Enter website's port: "))
            web_connect(web_ip,web_port)
            connection_check(web_ip)
        elif con_type=="quick_select_sites":
            print("Select a site to connect to:")
            a=input("\nGoogle, Facebook, YouTube, Amazon, Twitter, Reddit, GitHub, Stack Overflow, Instagram: ").lower()
            websites = {"google":"www.google.com","facebook":"www.facebook.com","youtube":"www.youtube.com","amazon":"www.amazon.com","twitter":"www.twitter.com","reddit":"www.reddit.com","github":"www.github.com","stack overflow":"www.stackoverflow.com","instagram":"www.instagram.com"}
            if a in websites:
                web_d=websites[a]
                web_ip=socket.gethostbyname(web_d)
                web_port=443
                web_connect(web_ip,web_port)
                connection_check(web_d)
            else:
                print("Invalid selection.")
        elif con_type=="simple_website":
            web_d=input("Enter website domain name: ")
            web_port=443
            web_ip=socket.gethostbyname(web_d)
            web_connect(web_ip,web_port)
            connection_check(web_d)
        elif con_type=="log_out":
            print("\nexiting program\n")
            main_page()
        elif con_type=="display_user_history":
            display_user_activity()
        else:
            print("Invalid connection type!")
            start_app()
    except Exception as e:
        print("Error in start_app:", e)
        main_page()


def main_page():
    try:
        a=input("\nSelect one: sign_up, login, create_database ")
        if a=="sign_up":
            signup()
        elif a=="login":
            login()
        elif a=="create_database":
            print("\nThis will overwrite the current database, are you sure?\n")
            warning=input("Select yes or no: ")
            if warning=="yes":   
                new()
                print("\nSuccessfully created a new database")
                main_page()
            else:
                print("\nReturning to main page")
                main_page()
        else:
            print("\nPlease select an input only from the above options !")
            main_page()
    except Exception as e:
        print("Error in main_page:", e)
a=(socket.gethostbyname(socket.gethostname()))
print("local host is connected to",a)
main_page()
