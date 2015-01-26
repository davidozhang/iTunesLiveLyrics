#!/usr/bin/python

'''
iTunes Live Lyrics Mac Terminal Client
Author: David Zhang
Version: 2.0
Last Updated: Jan 25, 2015
(C) Copyright David Zhang, 2015.
All lyrics fetched through the app belong to respective artists, owners,
Lyrics Wiki and Gracenote. I do not own any of the lyrics contents.
'''

from Foundation import *
from ScriptingBridge import *
from bs4 import BeautifulSoup as bs
import time
import re
import urllib
import requests
import StringIO

iTunes = SBApplication.applicationWithBundleIdentifier_("com.apple.iTunes")

class iTunesLiveLyricsSession:

	def query(self):
		apiFunctions = {'preview': 'getSong', 'hometown': 'getHometown'}
		artistQuery = queryFormat(self.artist)
		trackQuery = queryFormat(self.track)
		for key, function in apiFunctions.iteritems():
			apiURL = '{0}api.php?func={1}&artist={2}&song={3}&fmt=text'.format(
				self.root,
				function,
				urllib.quote(artistQuery),
				urllib.quote(trackQuery),
			)
			if key=='preview' and preview(apiURL)=='Not found':
				self.override=True
			elif key=='hometown' and preview(apiURL)=='':
				self.result[key] = 'N/A'
			else:
				self.result[key] = preview(apiURL)
		if not self.override:
			self.result['lyrics'] = sanitize(
										html(
											self.root,
											artistQuery,
											trackQuery,
										),
										self.result['preview'],
									)

	def header(self):
		lst = ['NOW PLAYING: {0} - {1}'.format(self.artist, self.track),
			   'Album: '+self.album,
			   'Genre: '+self.genre,
			   'Hometown: '+self.result['hometown']]
		wrap(lst)

	def lyrics(self):
		print self.result.get('lyrics', 'N/A')

	def displaySession(self):
		self.header()
		if self.override:
			print "No lyrics found!\n"
		else:
			self.lyrics()

	def __init__(self, *args, **kwargs):
		self.artist = kwargs.get('artist','N/A')
		self.track = kwargs.get('track', 'N/A')
		self.album = kwargs.get('album', 'N/A')
		self.genre = kwargs.get('genre', 'N/A')
		self.override = False
		self.root = 'http://lyrics.wikia.com/'
		self.result={}
		if len(kwargs)!=0:
			self.query()
			self.displaySession()

def html(root, artist, track):
	r = requests.get(root+artist+':'+track)
	return str(bs(r.text)).decode('utf_8')

def sanitize(html, firstLine):
	result = html[html.index(firstLine):html.index('<p>NewPP')]
	return str(bs(result.replace('<br/>','\n')).text.encode('utf_8'))

def preview(url):
	r = requests.get(url)
	buf = StringIO.StringIO(bs(r.text).text)
	return buf.readline().replace('\n','').replace('[...]','')

def queryFormat(item):
	result=''
	for i in range (0, len(item.split())):
		result+=item.split()[i]
		if i!=len(item.split())-1:
			result+='_'
	return result

def wrap(lst):
	border = ''
	max = 0
	for i in lst:
		if len(i)>max:
			max = len(i)
	border+='*'*(max+4)
	max+=4
	print '\n'+border
	for j in lst:
		print '| '+j+' '*(max-1-len('| '+j))+'|'
	print border+'\n'

def main():
	try:
		wrap(['Welcome to iTunesLiveLyrics client!', 'Version: 2.0'])
		session = iTunesLiveLyricsSession()
		while True:
			time.sleep(2)
			itunes = iTunes.currentTrack()
			if itunes.artist()!=session.artist or itunes.name()!=session.track:
				session = iTunesLiveLyricsSession(
					artist=itunes.artist(),
					track=itunes.name(),
					album=itunes.album(),
					genre=itunes.genre(),
				)
	except TypeError:
		wrap(['iTunesLiveLyrics detected no active iTunes song session.',
			  'Play your iTunes song then reload the client. Thanks!'])
	except:
		wrap(['iTunesLiveLyrics client has been closed.'])
	
if __name__=="__main__":
	main()