#Server.py

def file_read(x): #to read file
        f=open(x,"rb")
        msg=f.read()
        f.close()
        return msg

def file_append(y, z): #to add data to file
        t=open(y,"a")
        t.write(z)
        t.close()

def file_write(y, z): #to change all data in file
        t=open(y,"wb")
        t.write(z)
        t.close()
        
def ssl_socket(): #ssl socket
	serversocket.bind(("10.0.0.140",9889))  # use ip address of your network
	serversocket.listen(1)

	newsocket, fromaddr = serversocket.accept()
	recvso = ssl.wrap_socket(newsocket, server_side=True, certfile="/Users/Anvi/server.crt", 
	keyfile="/Users/Anvi/server.key", ssl_version=ssl.PROTOCOL_TLSv1)
	
	data_change(recvso)

def tcp_socket(): #tcp transmission
	serversocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	serversocket.bind(("10.0.0.140",9999))
	serversocket.listen(1)
	
	newsocket, fromaddr = serversocket.accept()
	data_change(newsocket)
		
def data_change(connstream):
	connstream.send("What is your client ID?") #asks for client id to save file for that name
	
	new_data = connstream.recv(1024)		#receives client id
	file_name= "/Users/Anvi/Documents/Project281/" + new_data + ".txt"	#creates client named file
	file_append(file_name, new_data) #adds client id in client's file
	
	msg=file_read(file_name) #reads client file and sends it back
	connstream.send(msg)
	new_data = connstream.recv(1024) #receives received from client to ensure data in file is correct or will return error in file
	
	if new_data == 'received':
		connstream.send("Do you want to add data?") #cient replies received asks if he wants to add data
		new_data = connstream.recv(1024)
		
		if new_data == 'yes' : #if client wants to add data adds it or ask if he wants to change data
			connstream.send("Send data")
			new_data = connstream.recv(1024)	#adds data to current file
			file_append(file_name, new_data)
			connstream.send("Data added")
			connstream.close()
			
		elif new_data == 'no' : #if client says no to add data asks if he wants to change data
			connstream.send("Do you want to change data?") #changes data if client says yes
			new_data = connstream.recv(1024)
			
			if new_data == 'yes':
				connstream.send("Send data")
				new_data = connstream.recv(1024)
				file_write(file_name, new_data)
				connstream.send("Data changed")
				connstream.close()
				
			else :
				connstream.send("Goodbye") #if there is no for changing data or any other answer then yes says goodbye and closes comnection
				connstream.close()	
		else :
				connstream.send("Goodbye") #if there is no 'yes' or 'no' for adding data considering error closes the connection by saying goodbye
				connstream.close()	
	else :
		connstream.send("Error in file") #if client don't reply received for file says error and closes connection
		connstream.close()	

#MAIN	
import socket
import sys
import ssl
import os

serversocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #server_socket

print "Do you want SECURE or INSECURE connection ? "
conn_type = str(raw_input())
conn_type=conn_type.upper()

if conn_type == 'SECURE':

    ssl_socket()

elif conn_type == 'INSECURE':

	tcp_socket()

else :
        print 'Incorrect Input …'



#Client.py
def datatransfer(clientssl):
	msg = clientssl.recv(1024) #receives ques for client id
	print (msg)			

	reply = str(raw_input()) #takes client id and send it to server
	clientssl.send(reply)			

	msg = clientssl.recv(1024)		#receives data in file ending with client's id
	print (msg)			

	reply=  str(raw_input()) #sends received if data ok and something else if data no ok
	clientssl.send(reply)

	msg = clientssl.recv(1024)		#receives ques to add data
	print (msg)			
	if msg == "Error in file":	#if received message is not add data but error in file then closes connection
		clientssl.close()

	else :
		reply=  str(raw_input()) #takes yes or no for adding data
		clientssl.send(reply)

		msg = clientssl.recv(1024)		#receives message either to send data for adding, goodbye or ques for changing data
		print (msg)	
		if msg == "Goodbye": 	#if received goodbye closes connection
			clientssl.close()
	
		else :
			reply=  str(raw_input())	#otherwise take data from client to send to server
			clientssl.send(reply)

			msg = clientssl.recv(1024)		#receives ques to change data, data added or goodbye
			print (msg)
			if msg == "Goodbye":	#if goodbye received closes connection
				clientsocket.close()
			
			elif msg == "Data added":		#if received data changed closes connection
				clientssl.close()
	
			else :
				reply=  str(raw_input())
				clientssl.send(reply)

				msg = clientssl.recv(1024)		#receives last message for data changed or goodbye and then closes connection
				print (msg)
				clientssl.close()		

def ssl_socket():
	clientsocket.connect(("10.0.0.221",9889))  
	clientssl1=ssl.wrap_socket(clientsocket, server_side=False, ca_certs='/Users/Anvi/server.crt', 
	cert_reqs=ssl.CERT_REQUIRED, ssl_version=ssl.PROTOCOL_TLSv1)
	datatransfer(clientssl1)

def tcp_socket():
	clientsocket.connect(("10.0.0.221",9999))	
	datatransfer(clientsocket)
	
#main
import socket
import sys
import ssl

clientsocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print "Do you want SECURE or INSECURE connection ? "
conn_type = str(raw_input())
conn_type=conn_type.upper()

if conn_type == 'SECURE':

    ssl_socket()

elif conn_type == 'INSECURE':

	tcp_socket()

else :
        print 'Incorrect Input …'






