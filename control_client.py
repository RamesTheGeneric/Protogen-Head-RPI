import socket
ip = "192.168.137.219"
port = 4269
msg = b"hello world"
print(f'Sending {msg} to {ip}:{port}')
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for i in range(1000000):

    sock.sendto(msg, (ip, port))