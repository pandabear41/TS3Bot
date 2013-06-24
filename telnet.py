class telnet():
    def connect(self):
        import telnetlib
        import ConfigParser
        #import io
        
        Config = ConfigParser.RawConfigParser(allow_no_value=False)
        Config.read('config.ini')
        
        User = Config.get('config', 'User')
        Pass = Config.get('config', 'Pass')
        Host = Config.get('config', 'Host')
        Port = Config.get('config', 'Port')
        Timeout = Config.get('config', 'Timeout')
        
        tn = telnetlib.Telnet(Host, Port, Timeout)
        
        
        