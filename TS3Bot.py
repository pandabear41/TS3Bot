'''
Created on Jun 24, 2013

@author: TReische
'''
import time
import telnet
import sys
import datetime
    
def main_loop():
    tn = telnet.telnet()
    tn.connect()
    

    while 1:
        seconds = int(datetime.datetime.now().strftime('%S')) % 30
        
        if seconds == 0:
            clist = tn.clientlist()
    
            for client in clist:
                idletime = tn.idletime(client)
                idletime = idletime / 60000
                if idletime >= 1:
                    time.sleep(1)
                    tn.move(client)
                    print "/n/rmoved client"
            
        time.sleep(0.1)
           
if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        sys.exit()
