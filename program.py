'''
Created on Jun 24, 2013

@author: TReische
'''

if __name__ == '__main__':
#    import sys
    import telnet
    
    user = "serveradmin"
    password = "GgDqiM3G"
    msg = None
    
    tn = telnet.telnet()
    tn.connect("halfcrap.com", "10011", 30)
    
    #tn = telnetlib.Telnet("halfcrap.com", "10011")      #Connect to the server
#    msg = tn.read_until("a specific command.")          #Wait until the welcome message is displayed
#    sys.stdout.write(msg)                               #Print the welcome message
    
#    tn.write("login " + user + " " + password + "\n")   #send login string
#    msg = tn.read_until("\n\rerror id=0 msg=ok", 2)
    
#    if msg == "\n\rerror id=0 msg=ok":
#        sys.stdout.write(msg.replace("\s"," "))
#        tn.write("use 1\n")
#        msg = tn.read_until("\n\rerror id=0 msg=ok")
#        sys.stdout.write('"' + msg.replace("\s"," ") + "'")
#        tn.write("quit\n")
#    else:
#        sys.stdout.write(msg.replace("\s", " "))
#        tn.write("quit\n")
#
#    print tn.read_all().replace("\s", " ")
    