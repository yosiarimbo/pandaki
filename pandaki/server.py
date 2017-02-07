import redis, httplib, urllib, sys, os, json
from twisted.internet import reactor, protocol
from flask import Flask, request
from time import time, sleep
from redis import Redis
from flask_redis import FlaskRedis
app2 = Flask(__name__)
r_server = redis.Redis('localhost')

user = {}

@app2.route('/api/serv1/v1.0/pandaki', methods=['GET'])
def all_user():
    data = ''
    all =  r_server.lrange('users', 0, -1)
    for i in all:
        data_user = r_server.hgetall(i)
        k = str(json.dumps(data_user))
        data += k
    print data
    return json.dumps(data)

@app2.route('/api/serv1/v1.0/pandaki/darurat/<string:username>', methods=['GET'])
def darurat(username):
    lat = str(r_server.hget(username, 'lat'))
    long = str(r_server.hget(username, 'long'))
    while True:
        print ('Pendaki dengan username: ' + username +' sedang mengalami posisi DARURAT posisi pendaki ada pada ' + lat + ' ' + long)
        sleep(2)
        if KeyboardInterrupt:
            return 'Silahkan memeriksa chat'



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

@app2.route('/api/serv1/v1.0/pandaki/<string:username>', methods=['GET'])
def get_user(username):
    user = r_server.hgetall(username)
    print r_server.hgetall('yosia')
    print user
    return json.dumps(user)

@app2.route('/api/serv1/v1.0/pandaki/lokasi/<string:username>', methods=['GET'])
def get_lokasi(username):
    lokasi = r_server.hmget(username, 'lat', 'long')
    #print r_server.hgetall('yosia')
    #print user
    return json.dumps(lokasi)

@app2.route('/api/serv1/v1.0/pandaki/<string:username>', methods=['DELETE'])
def delete_user(username):
    r_server.delete(username)
    r_server.lrem('users', username)
    if username in r_server.lrange('admin', 0, -1):
        r_server.lrem('admin', username)
        r_server.delete(username)
        return 'delete akun admin berhasil'
    if username in r_server.lrange('pendaki', 0, -1):
        r_server.lrem('pendaki', username)
        groupid = r_server.hget(username, 'groupid')
        groupid = str(groupid)
        #r_server.lrem('groups', username)
        r_server.lrem('group'+groupid, username)
        r_server.hdel(username, 'groupid')
        r_server.delete(username)
        return 'delete akun pendaki berhasil'
    else:
        return 'delete akun gagal'
    #id = str(userid)

    #return 'delete berhasil'

@app2.route('/api/serv1/v1.0/pandaki/group', methods=['POST'])
def create_group():
    cekid = r_server.lrange('groups', -1, -1)
    if not cekid:
        id = str(1)
    else:
        id = map(str, cekid)
        id = ''.join(id)
        id = int(id)+1
        id = str(id)
    r_server.rpush('groups', id)
    all_user()
    anggota = request.form.get('anggota')
    chunk = [user.strip() for user in anggota.split(',')]
    for user in chunk:
        print user
        r_server.hset(user, 'groupid', id)
        r_server.rpush('group:'+id, user)
    return 'buat grup berhasil'
    #print r_server.hget(username, 'groupid')
#cretae grup belum ada cek user nya kalo sudah ada grup nya gaggal
#belum masukin data idgrup ke usernya

@app2.route('/api/serv1/v1.0/pandaki/group/<string:groupid>', methods=['DELETE'])
def delete_group(groupid):
    user = r_server.lrange('group:'+groupid, 0, -1)
    for x in user:
        r_server.hdel(x, 'groupid')
    r_server.lrem('groups', groupid)
    r_server.delete('group:'+groupid)
    return 'Delete group berhasil'

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
                return 'user tidak ditemukan'
        else:
            return 'password salah'
    else:
        return 'username salah'

    return 'user tidak ditemukan'

if __name__ == '__main__':
    app2.run(debug=True)
    print 'jalan'