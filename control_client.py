import socket, pickle, argparse

def send(msg):
    data_string = pickle.dumps(msg)
    sock.sendto(data_string, (ip, port))


def start(ip):               #Implement BT server Code as TCP
    global port, sock, msg

    
    #ip = "protohead"
    #ip = socket.gethostbyname('localhost')
    print(f'control client ip: {ip}')
    port = 7171
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def main():
    while True:
        print('Commands: (Faces = face_#, overlay_#), (calibrate)')
        try:
            msg = input('Type Face: ')
        except: 
            print('couldent read msg')
        msg = msg.split()
        send(msg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='UDPCommandSender')
    parser.add_argument('--ip', help='The IP address of the host device you are trying to connect to.', default='localhost')
    args = parser.parse_args()
    ip = args.ip
    bluetooth = False
    start(ip)
    main()





