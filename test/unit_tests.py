#!/usr/bin/python

import sys
import os

from os import path
from nose.tools import assert_equal

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from ituneslivelyrics import *

def normal_test_no_album_no_genre():
	test = iTunesLiveLyricsSession(artist = 'Taylor Swift',
								   track = 'I Knew You Were Trouble')
	assert_equal(test.artist, 'Taylor Swift')
	assert_equal(test.track, 'I Knew You Were Trouble')
	assert_equal(test.album, 'N/A')
	assert_equal(test.genre, 'N/A')
	assert_equal(test.result['hometown'], 'Nashville')
	print test.result['lyrics']

def normal_test_no_album():
	test = iTunesLiveLyricsSession(artist = 'Taylor Swift',
								   track = 'Blank Space',
								   genre = 'Pop')
	assert_equal(test.artist, 'Taylor Swift')
	assert_equal(test.track, 'Blank Space')
	assert_equal(test.album, 'N/A')
	assert_equal(test.genre, 'Pop')
	assert_equal(test.result['hometown'], 'Nashville')
	print test.result['lyrics']

def normal_test_no_genre():
	test = iTunesLiveLyricsSession(artist = 'Taylor Swift',
								   track = 'Out Of The Woods',
								   album = '1989 (Deluxe Edition)')
	assert_equal(test.artist, 'Taylor Swift')
	assert_equal(test.track, 'Out Of The Woods')
	assert_equal(test.album, '1989 (Deluxe Edition)')
	assert_equal(test.genre, 'N/A')
	assert_equal(test.result['hometown'], 'Nashville')
	print test.result['lyrics']

def normal_test():
	test = iTunesLiveLyricsSession(artist = 'Taylor Swift',
								   track = 'Wildest Dreams',
								   album = '1989 (Deluxe Edition)',
								   genre = 'Pop')
	assert_equal(test.artist, 'Taylor Swift')
	assert_equal(test.track, 'Wildest Dreams')
	assert_equal(test.album, '1989 (Deluxe Edition)')
	assert_equal(test.genre, 'Pop')
	assert_equal(test.result['hometown'], 'Nashville')
	print test.result['lyrics']

def no_artist_test():
	test = iTunesLiveLyricsSession(artist = '',
								   track = 'TEST')
	assert_equal(test.artist, '')
	assert_equal(test.track, 'TEST')
	assert_equal(test.album, 'N/A')
	assert_equal(test.genre, 'N/A')
	assert_equal(test.result['preview'], 'N/A')
	assert_equal(test.result['lyrics'], 'N/A')

def invalid_artist_no_track_test():
	test = iTunesLiveLyricsSession(artist = 'DZ',
								   track = '')
	assert_equal(test.artist, 'DZ')
	assert_equal(test.track, '')
	assert_equal(test.album, 'N/A')
	assert_equal(test.genre, 'N/A')
	assert_equal(test.result['preview'], 'N/A')
	assert_equal(test.result['lyrics'], 'N/A')
