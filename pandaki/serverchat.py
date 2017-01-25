import redis, httplib, urllib, sys, os, json
from twisted.internet import reactor, protocol
from flask import Flask, request

app2 = Flask(__name__)
r_server = redis.Redis('localhost')

user = {}


class Chat(protocol.Protocol):
    def connectionMade(self):
        self.factory.clients.append(self)

    def connectionLost(self, reason):
        self.factory.clients.remove(self)

    def dataReceived(self, data):
        msg = ''
        kata = data.split()
        if (len(kata) >= 2):
            if (kata[0] == 'username'):
                self.lists(kata[1])
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
                for c in self.factory.clients:
                    if (self != c):
                        for x in range(2, len(pesan)):
                            msg += pesan[x]
                        c.message(kata[0] + ': ' + msg + '\n')
            elif (kata[1] == 'list'):
                for c in user:
                    msg += ('- ' + c + '\n')
                self.transport.write(msg)

    def lists(self, username):
        user[username] = self

    def message(self, message):
        self.transport.write(message)

def websocket():
    factory = protocol.ServerFactory()
    factory.protocol = Chat
    factory.clients = []
    reactor.listenTCP(6666, factory)
    reactor.run()

if __name__ ==  '__main__':
    websocket()