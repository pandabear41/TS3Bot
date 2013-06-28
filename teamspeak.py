import telnetlib
import sys
    
class TS3Client():
    clid = None             #client id            (based on connection order)
    cid = None              #channel id           (current channel id)
    idletime = None           #client idle time     (milliseconds)
    away = None             #client_away          (0|1)
    servergroups = []      #client_servergroups  (2,3,8)
    type = None             #client_type          (0 = normal|1 = serverquery)
    name = None
    
class TS3():
    tn = telnetlib.Telnet()
    accepted = "\n\rerror id=0 msg=ok"
    
    #connects to teamspeak and selects the virtual server
    def connect(self, User, Pass, Host, Port, VSID):
        self.tn.open(Host, Port)
        self.tn.read_until(".", 2) #wait until the welcome message is displayed
        
        self.tn.write("login " + User + " " + Pass + "\n")   #send login string
        msg = self.tn.read_until(self.accepted, 2)           #wait for login to be accepted or denied
        
        #if login is accepted select the virtual server
        if msg == self.accepted:
            self.tn.write("use " + VSID + "\n")
            msg = self.tn.read_until(self.accepted, 2)
            
            #if command is not accepted disconnect and return false
            if msg != self.accepted:
                print "\n\rError selecting virtual server " + VSID
                self.tn.write("logout\n")
                self.tn.read_until(self.accepted, 2)
                self.tn.write("quit\n")
                return False
            return True
        else:
            sys.stdout.write("\r\nError logging in. Please check your username and password.")
            sys.stdout.write(msg.replace("\s", " "))
            self.tn.write("quit\n")
            return False
        
    #gets a list of connected clients
    def clientlist(self):
        self.tn.write("clientlist\n")
        msg = self.tn.read_until(self.accepted, 2)
        msg = msg.replace(self.accepted, "")
        msg = msg.replace("\n\r", "")
        msg = msg.replace("|", " ")
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
                continue
                
            if m.find('client_idle_time=') > -1:
                c.idletime = int(m.replace('client_idle_time=','')) / 60000
                continue
                
            if m.find('client_servergroups=') > -1:
                c.servergroups = m.replace('client_servergroups=','').split(',')
                continue
                
            if m.find('client_away=') > -1:
                c.away = m.replace('client_away=','')
                continue
            
            if m.find('client_nickname=') > -1:
                c.name = m.replace('client_nickname=','')
                continue
                
            if m.find('client_type=') > -1:
                c.type = m.replace('client_away=','')
        return c
        
        
    def move(self, client, idle_channel):
        self.tn.write("clientmove clid=" + client + " cid=" + idle_channel + "\n")
        self.tn.read_until(self.accepted, 2)
        