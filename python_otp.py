import smtplib
import random
import pickle
import hashlib
from getpass import  getpass
try:
	with open('user1.p', 'rb') as fp:
	    data = pickle.load(fp)
	dict=data
except:
	print('couldnt find file creating one (please create a new user)')
	dict={}

def gen_otp():
	all=list(map(chr, range(48, 58)))+list(map(chr, range(65, 91)))+list(map(chr, range(97,123)))
	str=""
	for i in range(3):
		str=str+(random.choice(all))
		temp=str
	sh = hashlib.sha1()
	sh.update(str.encode())
	str = sh.hexdigest()
	with open('otp.p', 'wb') as fp:
		    pickle.dump(str, fp, protocol=pickle.HIGHEST_PROTOCOL)
	return temp

def send_otp(toaddrs):
	try:
		fromaddr = 'xyz@gmail.com'#senders address
		username = 'xyz@gmail.com'#username for app password account
		msg="""\
		Subject: OTP

		Your otp is   '{}'  .  Please do not share it with anyone.""".format(gen_otp())
		
		password ='jxsadfgrdgadf'#app password
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.starttls()
		
		server.login(username,password)
		server.sendmail(fromaddr, toaddrs, msg)
		server.quit()
		print('OTP send')
	except:
		pass



def check_otp(email):
	send_otp(email)
	with open('otp.p', 'rb') as fp:
		data = pickle.load(fp)
	otp=data
	user_otp = input()
	sh = hashlib.sha1()
	sh.update(user_otp.encode())
	user_otp = sh.hexdigest()
	i=3
	while True:
		if(user_otp==otp):
			return True
		else:
			print('invalid otp , You can try again {} times'.format(i))
			if(i==0):
				print('Your number of wrong attempts has crossed the limit ,Please restart entire process')
				break
			user_otp = input()
			sh = hashlib.sha1()
			sh.update(user_otp.encode())
			user_otp = sh.hexdigest()
			i-=1
	return False


def login():

			while True:
				username=input('enter username\t')
				if username in dict:
					break
				
				else:
					print('incorrect username please try again ')

			while True:
				password = getpass('enter password')
				sh = hashlib.sha1()
				sh.update(password.encode())
				password = sh.hexdigest()
				if(password!=dict[username][0]):
					print('incorrect credentials please try again')
				else:
					print('Sending OTP to registered mail')
					return check_otp(dict[username][1])




def create_new_user():
	while True:
		username=input('enter unique username\t')
		if username not in dict:
			break

		else:
			print('username already taken try something else')
	while True:
		email=input('enter an email')
		print('verify the email by putting the otp')
		if check_otp(email)==True:
			break
		else:
			print('incorrect verification')
	while True:
		password=getpass('enter password')
		c_password=getpass('confirm password')
		if(password==c_password):
			sh = hashlib.sha1()
			sh.update(password.encode())
			password = sh.hexdigest()
			break;
		else:
			print('passwords do not match')		
	dict[username]=[password,email]
	with open('user1.p', 'wb') as fp:
		pickle.dump(dict, fp, protocol=pickle.HIGHEST_PROTOCOL)






s=input('1.create new \n2.login\n')
create_new_user()
print('login')
if login()==True:
	print('logged in ')

