import redis, httplib, urllib, sys, os, json
from twisted.internet import reactor, protocol, task
from twisted.python import threadable
from flask import Flask, request
from txws import WebSocketFactory

app2 = Flask(__name__)
r_server = redis.Redis('localhost')

admin = {}
user = {}
pendaki = {}
list_thread = {}
darurat = []

class Chat(protocol.Protocol):
    print user
    def dataReceived(self, data):
        import time
        msg = ''
        print data
        kata = data.split()
        if (len(kata) >= 2):
            if (kata[0] == 'username'):
                self.lists(kata[1])
                if (kata[1] in r_server.lrange('admin', 0, -1)):
                    self.list_admin(kata[1])
                    print admin
                elif (kata[1] in r_server.lrange('pendaki', 0, -1)):
                    self.list_pendaki(kata[1])
                    print pendaki
            elif (kata[1] == 'darurat'):
                darurat.append(kata[0])
                print darurat
                if (darurat.count(kata[0]) == 3):
                    darurat.remove(kata[0])
                    darurat.remove(kata[0])
                    darurat.remove(kata[0])
                    username = str(r_server.hget(kata[0], 'username'))
                    lat = str(r_server.hget(kata[0], 'lat'))
                    long = str(r_server.hget(kata[0], 'long'))
                    thread = task.LoopingCall(Chat.darurat, pendaki[username], username, lat, long)
                    print thread.start(4.0)
                    list_thread[username] = thread
                    print list_thread

            elif (kata[1] == 'stop'):
                list_thread[kata[2]].stop()
                pendaki[kata[2]].message('Dimana mas?')


            elif (kata[1] == 'sendto'):
                print 'das'
                f = open('katakotor.txt', 'r')
                text = f.read()
                sentences = text.split()
                for stuff in sentences:
                    list = []
                    for x in range(0, len(stuff)):
                        list.append('*')
                        bintang = ''.join(list)
                    data = data.replace(stuff, bintang)
                f.close
                pesan = data.split()
                for c in user:
                    if (c == kata[2]):
                        print "ssss"
                        for x in range(3, len(pesan)):
                            msg += pesan[x]
                        user[c].message(kata[0] + ': ' + msg + '\n')
                        # if (self != c):
                        #	c.message(data[0])
            elif (kata[1] == 'broadcast'):
                f = open('katakotor.txt', 'r')
                text = f.read()
                sentences = text.split()
                for stuff in sentences:
                    list = []
                    for x in range(0, len(stuff)):
                        list.append('*')
                        bintang = ''.join(list)
                    data = data.replace(stuff, bintang)
                f.close
                pesan = data.split()
                print pesan
                for x in range(2, len(pesan)):
                    msg += ' ' + pesan[x]
                for c in user:
                    user[c].message(kata[0] + ': ' + msg + '\n')
            elif (kata[1] == 'chatgroup'):
                id = r_server.hget(kata[0], 'groupid')
                anggota = r_server.lrange('group:'+id, 0, -1)
                f = open('katakotor.txt', 'r')
                text = f.read()
                sentences = text.split()
                for stuff in sentences:
                    list = []
                    for x in range(0, len(stuff)):
                        list.append('*')
                        bintang = ''.join(list)
                    data = data.replace(stuff, bintang)
                f.close
                pesan = data.split()
                for x in range(2, len(pesan)):
                    msg += pesan[x]
                for c in anggota:
                    pendaki[c].message(kata[0] + ': ' + msg + '\n')

            elif (kata[1] == 'list'):
                for c in user:
                    msg += ('- ' + c + '\n')
                self.transport.write(msg)

    def lists(self, username):
        user[username] = self

    def list_pendaki(self, username):
        pendaki[username] = self

    def list_admin(self, username):
        admin[username] =self

    def message(self, message):
        self.transport.write(message)

    def darurat(self, username, lat, long):
        for x in admin:
            admin[x].message(
                'DARURAT PENDAKI DENGAN USERNAME ' + username + ' SEDANG MENGALAMI KEADAAN DARURAT PADA POSISI LATITUDE' + lat + ' LONGITUDE ' + long + '\n')

def websocket():
    factory = protocol.ServerFactory()
    factory.protocol = Chat
    #factory.clients = []
    reactor.listenTCP(6666, factory)
    reactor.listenTCP(9898, WebSocketFactory(factory))
    reactor.run()

if __name__ ==  '__main__':
    websocket()