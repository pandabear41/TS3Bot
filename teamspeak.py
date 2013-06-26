import telnetlib
import ConfigParser
import sys

tn = telnetlib.Telnet()
accepted = "\n\rerror id=0 msg=ok"
Config = ConfigParser.RawConfigParser(allow_no_value=False)
Config.read('config.ini')

class TS3():
    def connect(self):  
        #Read config properties
        User = Config.get('config', 'server_query_user')
        Pass = Config.get('config', 'server_query_pass')
        Host = Config.get('config', 'server_address')
        Port = Config.get('config', 'server_query_port')
        VID = Config.get('config', 'virtualserver_id')

        tn.open(Host, Port)
        msg = tn.read_until(".", 2) #wait until the welcome message is displayed
        sys.stdout.write(msg)       #print the welcome message
        
        tn.write("login " + User + " " + Pass + "\n")   #send login string
        msg = tn.read_until(accepted, 2)                #wait for login to be accepted or denied
        
        if msg == accepted:                         #if login is accepted
            sys.stdout.write(msg.replace("\s"," ")) #output message to console
            tn.write("use " + VID + "\n")           #select the virtual server
            msg = tn.read_until(accepted, 2)
            
            #if command is not accepted disconnect and return false
            if msg != accepted:
                sys.stdout.write("\n\rError selecting virtual server " + VID)
                tn.write("logout\n")
                tn.read_until(accepted, 2)
                tn.write("quit\n")
                return False
            
            #if virtual server is successfully selected print message to screen
            sys.stdout.write(msg.replace("\s"," "))
            return True
        else:
            sys.stdout.write("\r\nError logging in. Please check your username and password.")
            sys.stdout.write(msg.replace("\s", " "))
            tn.write("quit\n")
            return False
        
        
    def clientlist(self):
        #send the clientlist command and get the output
        tn.write("clientlist\n")
        msg = tn.read_until(accepted, 2)
        
        #remove the command accepted string
        msg = msg.replace(accepted, "")
        
        msg = msg.replace("\n\r", "")   #remove line breaks
        msg = msg.replace("|", " ")     #replace vertical bars with spaces
        msg = msg.split(' ')
        
        clist = []
        #get all client ids
        for client in msg:
            if client.find('clid=') > -1:
                clist.append(client.replace("clid=", ""))
                
        return clist
        
        
    def idletime(self, client):
        #send clientinfo command and get the output
        tn.write("clientinfo clid=" + client + "\n")
        msg = tn.read_until(accepted, 2)
        
        msg = msg.replace(accepted, "") #remove accepted message
        msg = msg.replace("\n\r", "")   #remove line breaks
        msg = msg.split(' ')
        
        #find the client idle time
        for idletime in msg:
            if idletime.find("client_idle_time=") > -1:
                idletime = idletime.replace("client_idle_time=", "")
                break
            else:
                idletime = -1
                
        return int(idletime)
        
        
    def move(self, client):
        cid = Config.get('config', 'afk_channel_id')
        tn.write("clientmove clid=" + client + " cid=" + cid)
        tn.read_until(accepted, 2)
        sys.stdout.write("/n/ruser moved")
        
        
        
        
        