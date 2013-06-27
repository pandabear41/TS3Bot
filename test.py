import teamspeak

if __name__ == '__main__':
    cli = tsclient.tsclient()
    ts = teamspeak.TS3()
    
    print dir(ts)
    print dir(cli)