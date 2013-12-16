import urllib, urllib2, cookielib
import time

username = 'jm8g08@soton.ac.uk'
password = 'quidditch1'


from requests import session

payload = {
    'action': 'login',
    'username': username,
    'password': password,
}

print session()

#with session() as c:
c.post('https://confluence.stsci.edu/login.action?os_destination=%252Fdashboard.action', data=payload)	
request = c.get('https://confluence.stsci.edu/display/StarWiki/PythonVersions')
print request.headers
print request.text
