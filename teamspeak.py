import telnetlib
import sys
    
class TS3Client():
    clid = '0'             #client id            (based on connection order)
    cid = '0'              #channel id           (current channel id)
    idletime = 0           #client idle time     (milliseconds)
    away = '0'             #client_away          (0|1)
    servergroups = []      #client_servergroups  (2,3,8)
    
class TS3():
    tn = telnetlib.Telnet()
    accepted = "\n\rerror id=0 msg=ok"
    
    def connect(self, User, Pass, Host, Port, VSID):
        accepted = self.accepted
        tn = self.tn
        
        tn.open(Host, Port)
        tn.read_until(".", 2) #wait until the welcome message is displayed
        
        tn.write("login " + User + " " + Pass + "\n")   #send login string
        msg = tn.read_until(accepted, 2)                #wait for login to be accepted or denied
        
        #if login is accepted select the virtual server
        if msg == accepted:
            tn.write("use " + VSID + "\n")
            msg = tn.read_until(accepted, 2)
            
            #if command is not accepted disconnect and return false
            if msg != accepted:
                print "\n\rError selecting virtual server " + VSID
                tn.write("logout\n")
                tn.read_until(accepted, 2)
                tn.write("quit\n")
                return False
            return True
        else:
            sys.stdout.write("\r\nError logging in. Please check your username and password.")
            sys.stdout.write(msg.replace("\s", " "))
            tn.write("quit\n")
            return False
        
        
    def clientlist(self):
        #send the clientlist command and get the output
        self.tn.write("clientlist\n")
        msg = self.tn.read_until(self.accepted, 2)
        
        msg = msg.replace(self.accepted, "") #remove the command accepted string
        msg = msg.replace("\n\r", "")   #remove line breaks
        msg = msg.replace("|", " ")     #replace vertical bars with spaces
        msg = msg.split(' ')
        
        clist = []
        #get all client ids and current channel ids
        for c in msg:
            if c.find('clid=') > -1:
                clist.append(c.replace('clid=',''))
        return clist
        

    def clientinfo(self, client):
        #send clientinfo command and get the output
        self.tn.write("clientinfo clid=" + client + "\n")
        msg = self.tn.read_until(self.accepted, 2)
             
        msg = msg.replace(self.accepted, "") #remove accepted message
        msg = msg.replace("\n\r", "")   #remove line breaks
        msg = msg.split(' ')
        
        c = TS3Client()
        
        c.clid = client
        #find the client idle time
        for m in msg:
            if m.find('cid=') > -1:
                c.cid = m.replace('cid=','')
                
            if m.find('client_idle_time=') > -1:
                c.idletime = int(m.replace('client_idle_time=','')) / 60000
                
            if m.find('client_servergroups=') > -1:
                c.servergroups = m.replace('client_servergroups=','').split(',')
                
            if m.find('client_away=') > -1:
                c.away = m.replace('client_away=','')
        return c
        
        
    def move(self, client, idle_channel):
        self.tn.write("clientmove clid=" + client + " cid=" + idle_channel + "\n")
        self.tn.read_until(self.accepted, 2)
        