import telnetlib
import ConfigParser
import sys

#Get config
Config = ConfigParser.RawConfigParser(allow_no_value=False)
Config.read('config.ini')

#Read config properties
User = Config.get('config', 'server_query_user')
Pass = Config.get('config', 'server_query_pass')
Host = Config.get('config', 'server_address')
Port = Config.get('config', 'server_query_port')
VID = Config.get('config', 'virtualserver_id')

#Set command accepted message
accepted = "\n\rerror id=0 msg=ok"

tn = telnetlib.Telnet(Host, Port)   #connect to server
    
class telnet():
    def connect(self):    

        msg = tn.read_until(".", 2)         #wait until the welcome message is displayed
        sys.stdout.write(msg)               #print the welcome message
        
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
                
            sys.stdout.write(msg.replace("\s"," "))
            return True
        else:
            sys.stdout.write("\r\nError logging in. Please check your username and password.")
            sys.stdout.write(msg.replace("\s", " "))
            tn.write("quit\n")
            return False
        