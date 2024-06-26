#import asyncio
import requests
from requests_html import HTMLSession
import re
from urllib3.exceptions import InsecureRequestWarning #when using verify=false and to get rid of warning messages because insecure

# [ ] pass url as argument
# [ ] handle requests error when SSL certificate check not passed (solution verify=False)
# [ ] Option to list all redirections or only final target url
#
url = 'http://bonvoyagenewsletter.com/KVqU.i?NXJdHWJrXxggHk=xzqGVXLWRkJnxYMWdjbHdyNjAxb3N0bzAxbGhobjB6MXQyMXAwYWxjN3p2ajA4dw=='
# url = 'http://bonvoyagenewsletter.com/GkgD.a?CbxmkdQQxGpnXS=bCTLSWwLwFmmbbMWdjbHdyNjAxb3NjNzAxbGhobjB6MXQyMXAwYWxjN3p4aWxjZA==' #redirect: 301
# url = 'https://find-mainstream-zone.life/?u=6c98hwq&o=u6wkrbr&m=1&t=maiendednew' #'http://www.organicfarmsamritsar.com/c/?&MJy3s2BwTomGMV100m4qCzlagg=de'

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

session = HTMLSession()

# Suppress the warnings from urllib3 when usin verify=false
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


# async def execWebpage(r):
	# print("async funct in progress...")
	# await renderPage(r)
	# print("async funct terminated...")

def check_redirect(url):
	noMoreRedirect = False

	while(noMoreRedirect == False):
		print("> Request HTML from", url)
		# r = requests.get(url, headers = headers, allow_requests = False)
		r = session.get(url, headers = headers, verify = False) # add verify=False to bypass SSL certificate check
		# print(r.html.render())
		# s = r.text
		s = r.html
		if (r.status_code > 300 and r.status_code < 400):
			print("> HTML response status code:",r.status_code)
			print(">> This code means: server redirection")
			r = requests.get(url, headers = headers)
			print(r.header.location)
			print(r.history)
			noMoreRedirect = True
		elif(r.status_code == 200):
			print("> HTML response status code:", r.status_code)
			print(">> This code means: HTML code (web page) received. OK!")
# Analyze HTML code received ....
			try:
				if re.search('window.location.replace',s).group() == 'window.location.replace':
					print("> HTML source code analysis: javascript detected")
					url = s.search('window.location.replace("{}")')[0]
					# log url into list called redir
					# redir.append(url)
					print("> URL redirected to:", url)
					noMoreRedirect = False
				elif re.search('<meta[^>]*?url=(.*?)["\']',s):
					print("> HTML source code analysis: Meta Tag redirect")
					
			except:
				# ajouter une étape de plus: r.html.render() pour interpreter le javascript de la page
				print("> URL redirected to:", s.url)
				# print(s.url)
#				print("No JS redir")
				noMoreRedirect = True
		else:
			noMoreRedirect = True

print("\nCheck for redirection for: ",url)
check_redirect(url)

#print(r.html.search('window.location.replace("{}")')[0])

	