import redis, httplib, urllib, sys, os, json
from twisted.internet import reactor, protocol
from flask import Flask, request
from redis import Redis
from flask_redis import FlaskRedis
app2 = Flask(__name__)
r_server = redis.Redis('localhost')

user = {}

@app2.route('/api/serv1/v1.0/pandaki', methods=['POST'])
def create_user():
    data = request.get_json('data')
    print data
    cekid = r_server.hvals('users')
    a = int(cekid[-1]) + 1
    id = str(a)
    r_server.hmset('user:'+id, data)
    r_server.hset('user:'+id, 'iduser', id)
    username = r_server.hget('user:'+id, 'username')
    r_server.hset('users', username, id)
    print r_server.hgetall('users')
    print r_server.hgetall('user:'+id)
    password = r_server.hget('user:'+id, 'pass')
    r_server.hset('pendaki', password, id)
    print r_server.hgetall('pendaki')
    return 'berhasil'

@app2.route('/api/serv1/v1.0/pandaki/<int:userid>', methods=['DELETE'])
def delete_user(userid):
    id = str(userid)
    username = r_server.hget('user:'+id, 'username')
    password = r_server.hget('user:'+id, 'password')
    r_server.hdel('users', username)
    r_server.hdel('pendaki', password)
    r_server.delete('user:'+id)
    return 'delete berhasil'

@app2.route('/api/serv1/v1.0/pandaki/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    print username, password
    userid = r_server.hget('users', username)
    a = str(userid)
    if (userid == None):
        #print userid
        return 'salah id'
    else :
        realpass  = r_server.hget('user:'+a, 'pass')
        if (password == realpass):
            admin = r_server.hget('auths', password)
            if (admin != None):
                return 'admin'
            else:
                pendaki = r_server.hget('pendaki', password)
                if (pendaki != None):
                    return 'pendaki'
                else:
                    return 'password salah'

    return 'user tidak ditemukan'

if __name__ == '__main__':
    app2.run(debug=True)
    print 'jalan'