import redis, httplib, urllib, sys, os, json
from twisted.internet import reactor, protocol
from flask import Flask, request
from redis import Redis
from flask_redis import FlaskRedis
app2 = Flask(__name__)
r_server = redis.Redis('localhost')

user = {}

def all_user():
    return r_server.lrange('users', 0, -1)

@app2.route('/api/serv1/v1.0/pandaki', methods=['POST'])
def create_user():
    data = request.get_json('data')
    username = data['username']
    print data
    print username
    if username in r_server.lrange('users',0,-1):
        return 'Coba Username lain'
    else:
        r_server.hmset(username, data)
        r_server.rpush('users', username)
        r_server.rpush('pendaki', username)
        print r_server.hgetall(username)
        print r_server.lrange('users', 0, -1)
        print r_server.lrange('pendaki', 0, -1)
        return 'tambah pendaki berhasil'

    #'''cekid = r_server.hvals('users')
    '''a = int(cekid[-1]) + 1
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
    return 'berhasil'''

@app2.route('/api/serv1/v1.0/pandaki/<string:username>', methods=['DELETE'])
def delete_user(username):
    r_server.delete(username)
    r_server.lrem('users', username)
    if username in r_server.lrange('admin', 0, -1):
        r_server.lrem('admin', username)
        return 'delete akun admin berhasil'
    if username in r_server.lrange('pendaki', 0, -1):
        r_server.lrem('pendaki', username)
        return 'delete akun pendaki berhasil'
    else:
        return 'delete akun gagal'
    #id = str(userid)
    '''username = r_server.hget('user:'+id, 'username')
    password = r_server.hget('user:'+id, 'password')
    r_server.hdel('users', username)
    r_server.hdel('pendaki', password)
    r_server.delete('user:'+id)'''
    #return 'delete berhasil'

@app2.route('/api/serv1/v1.0/pandaki/group', methods=['POST'])
def create_group():
    cekid = r_server.lrange('groups', -1, -1)
    if not cekid:
        a = str(1)
    else:
        a = map(str, cekid)
        a = ''.join(a)
        a = int(a)+1
        a = str(a)
    r_server.rpush('groups', a)
    all_user()
    anggota = request.form.get('anggota')
    chunk = [x.strip() for x in anggota.split(',')]
    for x in chunk:
        print x
        r_server.rpush('group:'+a, x)
    return 'buat grup berhasil'
    #print r_server.hget(username, 'groupid')

@app2.route('/api/serv1/v1.0/pandaki/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username in r_server.lrange('users',0,-1):
        cekpass = r_server.hget(username, 'pass')
        if (password == cekpass):
            statusadmin = r_server.lrange('admin', 0, -1)
            statuspendaki = r_server.lrange('pendaki', 0, -1)
            if username in statusadmin:
                return 'admin'
            if username in statuspendaki:
                return 'pendaki'
            else :
                'user tidak ditemukan'
        else:
            return 'password salah'
    else:
        return 'username salah'
    return 'user tidak ditemukan'
    '''print username, password
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
                    return 'password salah'''

    return 'user tidak ditemukan'

if __name__ == '__main__':
    app2.run(debug=True)
    print 'jalan'