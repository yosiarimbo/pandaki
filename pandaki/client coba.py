from prettytable import PrettyTable
import httplib, urllib, sys, os, json, redis, socket, select
r_server = redis.Redis('localhost')
conn = httplib.HTTPConnection("localhost:5000")
standby = True
status = ''
nama = ''
def prompt() :
	sys.stdout.write('<'+ username + '>')
	sys.stdout.flush()

def chat(username):
	host = '127.0.0.1'
	port = 6666
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	#username = raw_input('username :')
	s.send('username ' + username)
	print "- sendto nama_user pesan \n- broadcast pesan\n-list untuk melihat user aktif"

	while 1:
		socket_list = [sys.stdin, s]
		# Get the list sockets which are readable
		read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

		for sock in read_sockets:
			# incoming message from remote server
			if sock == s:
				data = sock.recv(4096)
				if not data:
					print '\nDisconnected from chat server'
					sys.exit()
				else:
					# print data
					sys.stdout.write('\n' + data)
					prompt()

			# user entered a message
			else:
				msg = sys.stdin.readline()
				s.send(username + ' ' + msg)
				prompt()

def darurat(username):
	conn.request("GET", "/api/serv1/v1.0/pandaki/darurat/"+str(username))
	response = conn.getresponse()
	print response.read()

def tambah_user(data):
	headers = {"Content-type": "application/json"}
	print data
	params = json.dumps(data)
	#params = urllib.urlencode(json)
	conn.request("POST", "/api/serv1/v1.0/pandaki", params, headers)
	response = conn.getresponse()
	#print headers
	#print params
	print response.read()

def semua():
	conn.request("GET", "/api/serv1/v1.0/pandaki")
	response = conn.getresponse()
	all_user = json.loads(response.read())
	print all_user
	indeks = len(all_user)
	x = PrettyTable(
		["ID", "Nama", "Gender", "HP", "Long", "Email", "GroupID", "Password", "Lat", "Alamat", "Penyakit", 'Umur'])
	x.align["ID"] = "l"  # Left align city names
	x.padding_width = 1  # One space between column edges and contents (default)
	for row in range(0, indeks, 12):
		x.add_row(all_user[row:row+12])
	print x


def get_user(username):
	conn.request("GET", "/api/serv1/v1.0/pandaki/"+str(username))
	response = conn.getresponse()
	user = json.loads(response.read())
	print user
	data = []
	x = PrettyTable(["ID", "Nama", "Penyakit", "Gender", "HP", "Lat", "GroupID", "Password", "Long", "Alamat", "Email", 'Umur'])
	x.align["ID"] = "l"  # Left align city names
	x.padding_width = 1  # One space between column edges and contents (default)
	for i in user:
		data.append(user[i])
	x.add_row(data)
	print x

def delete_user(username):
	conn.request("DELETE", "/api/serv1/v1.0/pandaki/"+str(username))
	response = conn.getresponse()
	print response.read()

def delete_group(groupid):
	#@app2.route('/api/serv1/v1.0/pandaki/group', methods=['POST'])
	conn.request("DELETE", "/api/serv1/v1.0/pandaki/group/"+str(groupid))
	response = conn.getresponse()
	print response.read()

def get_lokasi(username):
	conn.request("GET", "/api/serv1/v1.0/pandaki/lokasi/"+str(username))
	response = conn.getresponse()
	print response.read()

def login(username='', password=''):
	global status
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
	params = urllib.urlencode({'username': username, 'password': password})
	conn.request("POST", "/api/serv1/v1.0/pandaki/login", params, headers)
	response = conn.getresponse()
	#print headers
	#print params
	#print response.read()
	status = response.read()
	return status

def create_group(anggota=''):
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
	params = urllib.urlencode({'anggota': anggota})
	conn.request("POST", "/api/serv1/v1.0/pandaki/group", params, headers)
	response = conn.getresponse()
	print headers
	print params
	#print response.read()
	print response.read()


os.system('clear') #for linux
print '1. login '
print '2. register'
menu = input('silahkan pilih :')
if (menu==1):
	username = raw_input('username :')
	password = raw_input('password : ')
	#nama == username
	login(username, password)
	print status
	while standby is True:
		if (status == 'admin'):
			print "menu admin\n"
			print "1. Create User"
			print "2. Read Data User"
			print "3. Create Group"
			print "4. Delete Data User"
			print "5. Delete Group"
			print "6. Chat"
			menuadmin = input("Silahkan pilih : ")
			if (menuadmin==1):
				os.system('clear')  # for linux
				print "Create Data Pendaki Baru\n"
				username = raw_input('username: ')
				nama = raw_input('nama: ')
				password = raw_input('password : ')
				email = raw_input('email : ')
				alamat = raw_input('alamat : ')
				hp = raw_input('hp : ')
				umur = raw_input('umur : ')
				gender = raw_input('gender : ')
				penyakit = raw_input('penyakit : ')

				data = {'username': username, 'nama': nama, 'pass': password, 'gender': gender, 'alamat': alamat, 'HP': hp, 'umur': umur, 'email': email, 'penyakit': penyakit,
						'lat': '', 'long': '', 'groupid': ''}
				print data
				tambah_user(data)
			if (menuadmin==2):
				semua()
				username = raw_input('username :')
				get_user(username)
			if (menuadmin==3):
				anggota = raw_input('anggota :')
				create_group(anggota)
			if (menuadmin==4):
				username = raw_input('username :')
				delete_user(username)
			if (menuadmin==5):
				groupid = raw_input('groupid :')
				delete_user(groupid)
			if (menuadmin==6):
				chat(username)
		if (status == 'pendaki'):
			print "menu pendaki\n"
			print "1. Lokasiku"
			print "2. Chat "
			print "3. Darurat"
			menupendaki = input("Silahkan pilih : ")
			if (menupendaki==1):
				get_lokasi(username)
			if (menupendaki==2):
				chat(username)
			if (menupendaki==3):
				darurat(username)

	if (menu==2):
		os.system('clear')  # for linux
		print "Create Data Pendaki Baru\n"
		username = raw_input('username: ')
		nama = raw_input('nama: ')
		password = raw_input('password : ')
		email = raw_input('email : ')
		alamat = raw_input('alamat : ')
		hp = raw_input('hp : ')
		umur = raw_input('umur : ')
		penyakit = raw_input('penyakit : ')
		gender = raw_input('gender : ')
		data = {'username': username, 'nama': nama, 'pass': password, 'email': email, 'alamat': alamat, 'hp': hp,
				'umur': umur, 'penyakit': penyakit, 'gender': gender,
				'lat': '', 'long': '', 'groupid': ''}
		tambah_user(data)

	#print 'EXIT'
	if menu>3 or menu<0:
		loginstat="False"