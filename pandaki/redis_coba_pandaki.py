import redis
import json
from prettytable import PrettyTable
yosia = {'username': 'yosia', 'nama': 'Yosia Rimbo Deantama', 'pass': 'rimbo', 'email': 'yosiarimbo@gmail.com', 'alamat': 'Jl. Prigen No.3', 'HP': '082131234245', 'umur': '22', 'gender': 'L', 'penyakit': '-', 'lat': '', 'long': ''}
hanif = {'username': 'hanif', 'nama': 'Hanif Kuncahyo adi', 'pass': 'keceng', 'email': 'hanif@gmail.com', 'alamat': 'Jl. Berlian', 'HP': '081336052995', 'umur': '22', 'gender': 'L', 'penyakit': '-', 'lat': '', 'long': ''}
hudan = {'username': 'hudan', 'nama': 'Hudan Abdur Rohman', 'pass': 'abdur', 'email': 'hudan@gmail.com', 'alamat': 'Bandung Lautan Api', 'HP': '12345', 'umur': '22', 'gender': 'L', 'penyakit': '-', 'lat': '', 'long': '' }
nanda = {'username': 'nanda', 'nama': 'Nanda Romadhona', 'pass': 'nanda', 'email': 'nanda@gmail.com', 'alamat': 'Malang', 'HP': '081944829657', 'umur': '21', 'gender': 'P', 'penyakit': '-', 'lat': '', 'long': '' }

r_server = redis.Redis('localhost') #this line creates a new Redis object and
                                    #connects to our redis server
#r_server.set('test_key', 'test_value') #with the created redis object we can
                                        #submits redis commands as its methods
#resp_dict = json.loads(yosia)
print yosia['username'] # "ns1:timeSeriesResponseType"
#resp_dict['value']['queryInfo']['creationTime'] # 1349724919000
x = PrettyTable(["ID","Nama",'pass','email','gender','loc'])
x.align["ID"] = "l" # Left align city names
x.padding_width = 1 # One space between column edges and contents (default)
data = r_server.hvals('user:1')
r_server.delete('users')
r_server.delete('admin')
r_server.delete('pendaki')
r_server.hmset('yosia', yosia)
r_server.hmset('hanif', hanif)
r_server.hmset('hudan', hudan)
r_server.hmset('nanda', nanda)
r_server.rpush('la', 'yosia', 'hudan1')
r_server.rpush('users', 'yosia', 'hanif', 'hudan', 'nanda')
r_server.rpush('admin', 'yosia', 'hanif', 'hudan', 'nanda')
#r_server.lrem('users', 'yosia')
print r_server.hgetall('yosia')
print r_server.lrange('users', 0, -1)
print r_server.lrange('admin', 0, -1)
r_server.delete('asd')
if 'hudan' in r_server.lrange('la',0,-1):
    print 'ketemu'
else:
    print 'gagal'

#for row in data:
 #   x.add_row([row[0], row[1], row[2], row[3], row[4], row[5]])
#print x

#r_server.delete('user_names', 'user:1', 'user:2', 'user:3', 'user:10', 'pendaki', 'auths', 'users')

'''print r_server.hgetall('users')
r_server.rpush('hahahaha', 'aco')
print r_server.lrange('hahahaha', 0, -1)
r_server.hmset('user:1', admin)
r_server.hmset('user:2', user1)
#r_server.hmset('user:2', 'nama', 'hehe', 'at', 'ad')
r_server.hset('users', 'admin', 1)
r_server.hset('users', 'yosia', 2)
r_server.hset('auths', 'admin', 1)
r_server.hset('auths', 'rimbo', 2)
b = r_server.hvals('users')
print b[-1]
print r_server.hgetall('user:1')
print 'user:'+'3'
print r_server.hgetall('user:3')
print r_server.hgetall('user:3')
print r_server.hgetall('users')
print r_server.hgetall('pendaki')
print r_server.hlen('users')
print r_server.hgetall('coba')
print r_server.hgetall('tes')'''

'''r_server.zadd('user_names', 'Nilo', 1, 'Maria', 2)
r_server.zadd('user_emails', 'nilo@email.com', 1, 'maria@email.com', 2)
print r_server.zscore('user_emails', 'maria@email.com')
print  r_server.zrangebyscore('user_names', 2, 2)
r_server.hmset('test', {1: 'a', 2: {6: 'm'}})
r_server.hmset('test', m)
print r_server.hgetall('test')'''
'''r_server.hset('users', 'admin', 1)
r_server.hset('users', 'yosia', 2)
r_server.hset('users', 'coba', 3)
r_server.hset('user:1', 'admin', 'author')
r_server.hset('user:1', 'apa', 'ya')
r_server.hmset('user:2', user1)
r_server.hset('auths', 'author', 1)
r_server.hset('pendaki', 'rimbo', 2)
print r_server.hgetall('users')
print r_server.hgetall('user:10')
a = r_server.hget('user:10', 'iduser')
c = r_server.hget('user:10', 'username')
print a
r_server.hset('users', c, a)
print r_server.hgetall('users')
print r_server.hmget('user:2', 'username', 'gender', 'location')

username = raw_input('username :')
userid = r_server.hget('users', username)
a = str(userid)
if (userid == None):
    print 'salah id'
password = raw_input('pass :')

realpass = r_server.hget('users:'+a, 'admin')
if (password == None):
    print 'salah pass'
else:
    print 'berhasil login'''''


