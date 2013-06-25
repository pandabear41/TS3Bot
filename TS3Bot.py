'''
Created on Jun 24, 2013

@author: TReische
'''
import time
import telnet
import sys

def main_loop():
    tn = telnet.telnet()
    tn.connect()
        
    while 1:
        time.sleep(0.1)
           

if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        sys.exit() 