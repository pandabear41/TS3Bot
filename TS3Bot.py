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
    sq_user = None
    sq_pass = None
    sq_port = None
    server_address = None
    vsid = None
    idle_cid = None
    update_interval = None
    
def ReadConfig():
    Config = ConfigParser.RawConfigParser(allow_no_value=False)
    Config.read('config.ini')
    
    conf = cfg()
    conf.sq_user = Config.get('config', 'server_query_user')
    conf.sq_pass = Config.get('config', 'server_query_pass')
    conf.sq_port = Config.get('config', 'server_query_port')
    conf.server_address = Config.get('config', 'server_address')
    conf.vsid = Config.get('config', 'virtualserver_id')
    conf.idle_cid = Config.get('config', 'idle_channel_id')
    conf.update_interval = int(Config.get('config', 'update_interval'))
    return conf
    
def main_loop():
    conf = ReadConfig()
    ts = teamspeak.TS3()
    ts.connect(conf.sq_user, conf.sq_pass, conf.server_address, conf.sq_port, conf.vsid)
    
    while 1:
        seconds = int(datetime.datetime.now().strftime('%S')) % conf.update_interval
        
        if seconds == 0:
            clist = ts.clientlist()
            for c in clist:
                client = ts.clientinfo(c)
                if client.idletime >= 180 and client.cid != cfg.idle_cid and client.type != '1':
                    ts.move(c, conf.idle_cid)

        time.sleep(0.1)
           
           
if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        sys.exit()
