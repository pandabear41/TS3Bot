'''
Created on Jun 24, 2013

@author: TReische
'''
import time
import sys
import datetime
import teamspeak
    
def main_loop():
    ts = teamspeak.TS3()
    ts.connect()

    while 1:
        seconds = int(datetime.datetime.now().strftime('%S')) % 30
        
        if seconds == 0:
            clist = ts.clientlist()

            for client in clist:
                #get client idle time and convert to minutes
                idletime = ts.idletime(client)
                idletime = idletime / 60000
                
                if idletime >= 1:
                    time.sleep(1)   #wait 1 second between commands to prevent autoban
                    ts.move(client)
                    print "/n/rmoved client"
            
        time.sleep(0.1)
           
if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        sys.exit()
