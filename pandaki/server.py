import redis, httplib, urllib, sys, os, json
from twisted.internet import reactor, protocol
from flask import Flask, request
from time import time, sleep
from redis import Redis
from flask_redis import FlaskRedis
from datetime import datetime
app2 = Flask(__name__)
r_server = redis.Redis('localhost')

user = {}

@app2.route('/api/serv1/v1.0/pandaki', methods=['GET'])
def all_user():
    user = []
    data = ''
    all =  r_server.lrange('users', 0, -1)
    for i in all:
        data_user = r_server.hgetall(i)
        #k = str(json.dumps(data_user))
        #data += k
        user.append(data_user)
    print data
    return json.dumps(user)

@app2.route('/api/serv1/v1.0/pandaki/pendaki', methods=['GET'])
def all_user_pendaki():
    data = ''
    all =  r_server.lrange('pendaki', 0, -1)
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
        r_server.rpush('tempuser', username)
        #r_server.rpush('users', username)
        #r_server.rpush('pendaki', username)
        print r_server.hgetall(username)
        print r_server.lrange('users', 0, -1)
        print r_server.lrange('pendaki', 0, -1)
        return 'tambah pendaki berhasil'

    #'''cekid = r_server.hvals('users')

@app2.route('/api/serv1/v1.0/pandaki/infotips', methods=['POST'])
def create_info():
    data = request.get_json('data')
    tipe = data['tipe']
    if tipe == 'info':
        if len(r_server.lrange('idinfo', 0, -1)) == 0:
            id = '1'
            time = str(datetime.now())
            r_server.rpush('idinfo', id)
            r_server.hmset('info:'+id, data)
            r_server.hset('info:'+id, 'time', time)
            print r_server.lrange('idinfo', 0, -1)
            print r_server.hgetall('info:'+id)
            return 'Create Info Berhasil'
        else:
            id = r_server.lrange('idinfo', -1, -1)
            id = " ".join(str(x) for x in id)
            id = int(id) + 1
            id = str(id)
            time = str(datetime.now())
            r_server.rpush('idinfo', id)
            r_server.hmset('info:'+id, data)
            r_server.hset('info:'+id, 'time', time)
            print r_server.lrange('idinfo', 0, -1)
            print r_server.hgetall('info:'+id)
            return 'Create Info Berhasil'
    elif tipe == 'tips':
        if len(r_server.lrange('idtips', 0, -1)) == 0:
            id = '1'
            time = str(datetime.now())
            r_server.rpush('idtips', id)
            r_server.hmset('tips:'+id, data)
            r_server.hset('tips:'+id, 'time', time)
            print r_server.lrange('idtips', 0, -1)
            print r_server.hgetall('tips:'+id)
            return 'Create Tips Berhasil'
        else:
            id = r_server.lrange('idtips', -1, -1)
            id = " ".join(str(x) for x in id)
            id = int(id) + 1
            id = str(id)
            time = str(datetime.now())
            r_server.rpush('idtips', id)
            r_server.hmset('tips:'+id, data)
            r_server.hset('tips:'+id, 'time', time)
            print r_server.lrange('idtips', 0, -1)
            print r_server.hgetall('tips:'+id)
            return 'Create Tips Berhasil'
    else:
        return 'Create Tips atau Info Gagal'

@app2.route('/api/serv1/v1.0/pandaki/infotips/info', methods=['GET'])
def all_info():
    info = []
    data = ''
    all =  r_server.lrange('idinfo', 0, -1)
    for i in all:
        data_info = r_server.hgetall('info:'+i)
        #k = str(json.dumps(data_user))
        #data += k
        info.append(data_info)
    print data
    return json.dumps(info)

@app2.route('/api/serv1/v1.0/pandaki/infotips/tips', methods=['GET'])
def all_tips():
    tips = []
    data = ''
    all = r_server.lrange('idtips', 0, -1)
    for i in all:
        data_info = r_server.hgetall('tips:' + i)
        # k = str(json.dumps(data_user))
        # data += k
        tips.append(data_info)
    print data
    return json.dumps(tips)

@app2.route('/api/serv1/v1.0/pandaki/infotips/info<string:id>', methods=['DELETE'])
def delete_info(id):
    r_server.delete('info:'+id)
    r_server.lrem('idinfo', id)
    print r_server.lrange('idinfo', 0, -1)
    print r_server.hgetall('info:' + id)
    return 'Delete info berhasil'

@app2.route('/api/serv1/v1.0/pandaki/infotips/tips<string:id>', methods=['DELETE'])
def delete_tips(id):
    r_server.delete('tips:'+id)
    r_server.lrem('idtips', id)
    print r_server.lrange('idtips', 0, -1)
    print r_server.hgetall('tips:' + id)
    return 'Delete tips berhasil'

@app2.route('/api/serv1/v1.0/pandaki/validasi', methods=['POST'])
def validasi():
    username = request.get_json('username')
    print r_server.lrange('tempuser', 0, -1)
    if username in r_server.lrange('tempuser', 0, -1):
        r_server.rpush('users', username)
        r_server.rpush('pendaki', username)
        r_server.lrem('tempuser', username)
        return 'Proses validasi berhasil'
    else:
        return 'User tidak terdaftar'

@app2.route('/api/serv1/v1.0/pandaki/<string:username>', methods=['GET'])
def get_user(username):
    user = r_server.hgetall(username)
    print r_server.hgetall('yosia')
    print user
    return json.dumps(user)

@app2.route('/api/serv1/v1.0/pandaki/infotips/info<string:id>', methods=['GET'])
def get_info(id):
    info = r_server.hgetall('info:'+id)
    return json.dumps(info)

@app2.route('/api/serv1/v1.0/pandaki/infotips/tips<string:id>', methods=['GET'])
def get_tips(id):
    tips = r_server.hgetall('tips:'+id)
    return json.dumps(tips)

@app2.route('/api/serv1/v1.0/pandaki/lokasi/<string:username>', methods=['GET'])
def get_lokasi(username):
    lokasi = r_server.hmget(username, 'lat', 'long')
    #print r_server.hgetall('yosia')
    #print user
    return json.dumps(lokasi)

@app2.route('/api/serv1/v1.0/pandaki/infotips/info', methods=['PUT'])
def update_info():
    id = request.form.get('id')
    judul = request.form.get('judul')
    konten = request.form.get('konten')
    foto = request.form.get('foto')
    time = str(datetime.now())
    r_server.hmset('info:'+id, {'judul': judul, 'konten': konten, 'foto': foto, 'time': time})
    return 'update info berhasil'

@app2.route('/api/serv1/v1.0/pandaki/infotips/tips', methods=['PUT'])
def update_tips():
    id = request.form.get('id')
    judul = request.form.get('judul')
    konten = request.form.get('konten')
    foto = request.form.get('foto')
    time = str(datetime.now())
    r_server.hmset('tips:'+id, {'judul': judul, 'konten': konten, 'foto': foto, 'time': time})
    return 'update info berhasil'

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

    #all_user()
    anggota = request.form.get('anggota')
    isi = str(anggota)
    #print isi
    chunk = [user.strip() for user in anggota.split(',')]
    #print chunk[0]
    #print chunk[1]
    print len(chunk)
    print user
    for users in chunk:
        print users
        if (r_server.hget(users, 'groupid') == ''):
            r_server.rpush('groups', id)
            r_server.hset(users, 'groupid', id)
            r_server.rpush('group:' + id, users)
            #return 'buat grup berhasil'
        if (r_server.hget(users, 'groupid') == None):
            return 'User ' +users+ ' tidak ada'
    return 'buat grup berhasil'
    #print r_server.hget(username, 'groupid')
#cretae grup belum ada cek user nya kalo sudah ada grup nya gaggal
#belum masukin data idgrup ke usernya

@app2.route('/api/serv1/v1.0/pandaki/group/<string:groupid>', methods=['DELETE'])
def delete_group(groupid):
    if groupid in r_server.lrange('groups', 0, -1):
        user = r_server.lrange('group:'+groupid, 0, -1)
        for x in user:
            r_server.hset(x, 'groupid', '')
        r_server.lrem('groups', groupid)
        r_server.delete('group:'+groupid)
        return 'Delete group berhasil'
    else:
        return 'Delete group gagal'

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
        return 'username tidak ditemukan'


if __name__ == '__main__':
    app2.run(debug=True)
    print 'jalan'