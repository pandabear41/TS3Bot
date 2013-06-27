'''
Created on Jun 24, 2013

@author: TReische
'''
import time
import sys
import datetime
import ConfigParser
import teamspeak

class cfg():
    sq_user = ''
    sq_pass = ''
    sq_port = ''
    server_address = ''
    vsid = ''
    afk_channel = ''
    
def ReadConfig():
    Config = ConfigParser.RawConfigParser(allow_no_value=False)
    Config.read('config.ini')
    
    cfg.sq_user = Config.get('config', 'server_query_user')
    cfg.sq_pass = Config.get('config', 'server_query_pass')
    cfg.sq_port = Config.get('config', 'server_query_port')
    cfg.server_address = Config.get('config', 'server_address')
    cfg.vsid = Config.get('config', 'virtualserver_id')
    cfg.idle_cid = Config.get('config', 'idle_channel_id')

    
def main_loop():
    ReadConfig()
    print cfg.afk_channel
    
    ts = teamspeak.TS3()
    ts.connect(cfg.sq_user, cfg.sq_pass, cfg.server_address, cfg.sq_port, cfg.vsid)
    
    while 1:
        seconds = int(datetime.datetime.now().strftime('%S')) % 30
        
        if seconds == 0:
            clist = ts.clientlist()
            for c in clist:
                client = ts.clientinfo(c)
                if client.idletime >= 1 and client.cid != cfg.idle_cid:
                    ts.move(c, cfg.idle_cid)
            
        time.sleep(0.1)
           
           
if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        sys.exit()
