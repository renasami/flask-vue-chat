import socket
ip = socket.gethostname()
print(ip)
addr = socket.gethostbyname(ip)
print(addr)