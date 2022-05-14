import socket, pickle

def send(msg):
    ip = "192.168.137.219"
    port = 4269
    print(f'Sending {msg} to {ip}:{port}')
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data_string = pickle.dumps(msg)
    sock.sendto(data_string, (ip, port))

def main():
    while True:
        print('Faces = face_#, blush_#')
        msg = input('Type Face: ')
        msg = msg.split()
        send(msg)

main()