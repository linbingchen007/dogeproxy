import socket
import sys
import threading
import re
cache={}
threads=[]
def s2cworker(nsock,connection):
    print "receiving data from server"
    while True:
        print "----------receive------------"
        print 'server:  '+data
        ssdata = nsock.recv(65535)
        #print len(ssdata)
        #print 'ssdata:'+ssdata

        if ssdata and len(ssdata):
            connection.sendall(ssdata)                    
        else:
            break
    print "exit thread"
    nsock.close()
    connection.close()
    return 

def c2sworker(connection):
    try:
        while True:
            data = connection.recv(65535)   
            if not (data and len(data)):
                break
            print "----------send------------"
            print 'client:  '
            print repr(data)
            remoteaddr = re.search(r'Host:\s*([^\n\r]*)\s*[\r\n]+',data)
            if remoteaddr:
                remoteaddr=remoteaddr.group(1)
            else:
                break   
            print remoteaddr
            nsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            nsaddr = (remoteaddr,80)
            nsock.connect(nsaddr)
            nsock.settimeout(4)
            nsock.sendall(data)
            print "receiving data from server"
            rawdata = ''
            print "*****************************************"
            try:
                while True:
                    ssdata = nsock.recv(65534)
                    """
                    sslen = re.search(r'Content-Length:\s*([0-9]+)\s*\r\n'):
                    if sslen and len(sslen):
                        sslen = int(sslen.group(1))
                        rawdata = ssdata[ssdata.find('\r\n\r\n')+4:]
                        fg=True
                        sslen-=len(rawdata)
                    else:
                        pass
                    """

                    print "----------receive------------"
                    print 'server:  '
                    print repr(ssdata)
                    #print len(ssdata)
                    #print 'ssdata:'+ssdata

                    if ssdata and len(ssdata):
                        connection.sendall(ssdata)                    
                    else:                
                        break
            except:
                pass
            finally:
                nsock.close()
            print "##############################################"
            print "exit thread"
    except:
        pass
    finally:
        connection.close()  
        return 

    
     

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_address = ('localhost',16200)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
sock.listen(100)
while True:
    print  'waiting for a connection'
    connection , client_address =  sock.accept()
    connection.settimeout(4)
    print  'connection from',client_address
    print "receiving data from client"
    t = threading.Thread(target=c2sworker,args=(connection,)) 
    #threads.append(t)
    t.start()

