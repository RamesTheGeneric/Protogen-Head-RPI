import OPi.GPIO as GPIO
import time
import os
import subprocess
import signal

BOARD = {
3: 71,
5: 72,
7: 75,
11: 146,
13: 150,
15: 149,
19: 40,
21: 39,
23: 41,
27: 64,
29: 74,
31: 73,
33: 76,
35: 133,
37: 158,
8: 148,
10: 147,
12: 131,
16: 100,
18: 148,
22: 157,
24: 42,
28: 65,
32: 112,
36: 132,
38: 134,
40: 135,
}

GPIO.setmode(BOARD)
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
run = False
command = "python main.py"
while True:
    try:
        if GPIO.input(16):  #Button pressed
            print('Input was HIGH')
            if run: pass
            else: 
                p=subprocess.Popen(command, shell=True, preexec_fn=os.setsid) 
                run = True
        else:               # Button Released
            print('Input was LOW')
            if run: 
                os.killpg(p.pid, signal.SIGTERM)
                run = False
            else: pass
    except Exception as e: print(e)
    time.sleep(1)
GPIO.cleanup()