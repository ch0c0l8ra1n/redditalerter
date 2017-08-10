re_username = "" #your reddit usename
re_password = "" #your reddit password

g_username = "" # your gmail username
g_password = "" # your gmail password

sendwho = "" # whom do you want to send the email to, You can use same email to both send and receive emails

subreddit = "r/forhire" #which subreddit you want to scan?

t_inter = 2 #timeout in seconds afte no new posts are found, recommended value 2

print("Initializing...")
import json
import urllib.request
from http.cookiejar import CookieJar
import time
import smtplib
import email

import functools
print = functools.partial(print, flush=True)

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE

#logging in to gmail 
smtp_host = 'smtp.gmail.com'
smtp_port = 587
server = smtplib.SMTP()
server.connect(smtp_host,smtp_port)
server.ehlo()
server.starttls()
user=g_username
passw = g_password
server.login(user,passw)
fromaddr= g_username
tolist = sendwho

#login and config
user = re_username
passwad = re_password
limit=1
info = []
i=1

# setting up a virtual browser kinda thing and logging into your account
usagent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
cj = CookieJar()
opener= urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent',usagent)]
urllib.request.install_opener(opener)
authentication_url = 'https://ssl.reddit.com/post/login'
payload = {
	'op':'username',
	'user': user,
	'passwd': passwad
}

data = urllib.parse.urlencode(payload)
binary_data = data.encode('UTF-8')
req = urllib.request.Request(authentication_url, binary_data)
print("Logging in...")
resp = urllib.request.urlopen(req)
url = "https://www.reddit.com/api/me.json"
response = urllib.request.urlopen(url)
your_json = response.read()
parsed = json.loads(your_json.decode())
uhash= (parsed["data"]["modhash"])
print("Logged in as :"+parsed["data"]["name"])
before=""

#getting latest post of so subreddit
link  = "https://www.reddit.com/"+subreddit+"/new/.json?limit="+str(1)
response = urllib.request.urlopen(link)
your_json = response.read()
parsed = json.loads(your_json.decode())
#print(parsed)
before =  parsed["data"]["children"][0]["data"]["id"]
print("Latest post in the subreddit:\n"+parsed["data"]["children"][0]["data"]["title"])

message = '<html><head></head><body><p>You are now scanning '+subreddit+'<br><br>Latest post:<br><br><a href="https://reddit.com'+parsed["data"]["children"][0]["data"]["permalink"]+'">'+parsed["data"]["children"][0]["data"]["title"]+'</a></p><p>'+parsed["data"]["children"][0]["data"]["selftext"]+'</p></body></html>'

msg =MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = COMMASPACE.join(tolist)
msg['Subject'] = "Program Started"
msg.attach(MIMEText(message,'html'))
#msg.attach(MIMEText('\nsent via python', 'plain'))
server.sendmail(user,tolist,msg.as_string())

while True:

	link  = "https://www.reddit.com/"+subreddit+"/new/.json?limit="+str(limit)+"&before=t3_"+before

	response = urllib.request.urlopen(link)
	your_json = response.read()
	parsed = json.loads(your_json.decode())


	if len(parsed["data"]["children"])==0:
		print("Z",end="")
		time.sleep(t_inter)
		continue
	print()

	message = '<html><head></head><body><p><a href="https://reddit.com'+parsed["data"]["children"][0]["data"]["permalink"]+'">'+parsed["data"]["children"][0]["data"]["title"]+'</a></p><p>'+parsed["data"]["children"][0]["data"]["selftext"]+'</p></body></html>'
	msg =MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = COMMASPACE.join(tolist)
	msg['Subject'] = "New post in " + subreddit  
	msg.attach(MIMEText(message,'html'))
	server.sendmail(user,tolist,msg.as_string())

	before =  parsed["data"]["children"][0]["data"]["id"]
	time.sleep(t_interval)



