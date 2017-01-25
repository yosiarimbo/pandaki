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

def tambah_user(data):
	headers = {"Content-type": "application/json"}
	print data
	params = json.dumps(data)
	#params = urllib.urlencode(json)
	conn.request("POST", "/api/serv1/v1.0/pandaki", params, headers)
	response = conn.getresponse()
	print headers
	print params
	print response.read()

def semua():
	conn.request("GET", "/api/serv1/v1.0/pandaki")
	response = conn.getresponse()
def delete_user(userid):
	conn.request("DELETE", "/api/serv1/v1.0/pandaki/"+str(userid))
	response = conn.getresponse()
	print response.read()

def login(username='', password=''):
	global status
	headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
	params = urllib.urlencode({'username': username, 'password': password})
	conn.request("POST", "/api/serv1/v1.0/pandaki/login", params, headers)
	response = conn.getresponse()
	print headers
	print params
	#print response.read()
	status = response.read()
	return status

while standby is True:
	os.system('clear') #for linux
	print '1. login '
	print '2. register'
	menu = input('silahkan pilih :')
	if (menu==1):
		username = raw_input('username :')
		password = raw_input('password : ')
		nama == username
		login(username, password)
		print status
		if (status == 'admin'):
			print "menu admin\n"
			print "1. Create User"
			print "2. Read Data User"
			print "3. Update Data User"
			print "4. Delete Data User"
			print "5. Chat"
			menu = input("Silahkan pilih : ")
			if (menu==1):
				os.system('clear')  # for linux
				print "Create Data Pegawai Baru\n"
				username = raw_input('username: ')
				password = raw_input('password : ')
				email = raw_input('email : ')
				gender = raw_input('gender : ')
				data = {'iduser': '', 'username': username, 'pass': password, 'email': email, 'gender': gender,
						'location': ''}
				tambah_user(data)
			if (menu==2):
				print 'read semua user'
				semua()
			if (menu==4):
				userid = raw_input('id pendaki :')
				delete_user(userid)
			if (menu==5):
				chat(username)
		if (status == 'pendaki'):
			print "menu pendaki\n"
			print "1. Edit profile"
			print "2. Chat "
			menu = input("Silahkan pilih : ")
			if (menu==2):
				chat(username)
	if (menu==2):
		os.system('clear')  # for linux
		print "Create Data Pegawai Baru\n"
		username = raw_input('username: ')
		password = raw_input('password : ')
		email = raw_input('email : ')
		gender = raw_input('gender : ')
		data = {'iduser': '', 'username': username, 'pass': password, 'email': email, 'gender': gender, 'location': ''}
		tambah_user(data)


	print 'EXIT'

	if menu>4 or menu<0:
		loginstat="False"