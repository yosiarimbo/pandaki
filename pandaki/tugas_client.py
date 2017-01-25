import socket, select, string, sys

def prompt() :
	sys.stdout.write('<'+ username + '>')
	sys.stdout.flush()

#main function
if __name__ == "__main__":
	
	host = '127.0.0.1'
	port = 6666
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	username = raw_input('username :')
	s.send('username ' + username) 
	print "- sendto nama_user pesan \n- broadcast pesan\n-list untuk melihat user aktif"
		   
	while 1:
		socket_list = [sys.stdin, s]
		# Get the list sockets which are readable
		read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
		
		for sock in read_sockets:
			#incoming message from remote server
			if sock == s:
				data = sock.recv(4096)
				if not data :
					print '\nDisconnected from chat server'
					sys.exit()
				else :
					#print data
					sys.stdout.write('\n' + data)
					prompt()
			
			#user entered a message
			else :
				msg = sys.stdin.readline()
				s.send(username + ' ' + msg)
				prompt()