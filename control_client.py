import socket, pickle

def send(msg):
    data_string = pickle.dumps(msg)
    sock.sendto(data_string, (ip, port))

def start():
    if bluetooth == False:                  #Implement BT server Code as TCP
        global ip, port, sock, msg

        ip = "192.168.137.219"
        port = 4269
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        ip = 'DC:A6:32:20:8B:CD'
        port = 1
        sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_SEQPACKET, socket.BTPROTO_L2CAP)  #socket.SOCK_STREAM
        #sock.connect((ip, port))
def main():
    while True:
        print('Faces = face_#, overlay_#')
        msg = input('Type Face: ')
        msg = msg.split()
        send(msg)


if __name__ == "__main__":

    bluetooth = True
    start()
    main()





