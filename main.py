import os,sys


#Temporary workaround
try:
    info = open('./data/info.txt')
except IOError:
    print 'It looks you only have the source but no data. Want me to get that for you?'
    getData = raw_input('data directory missing. want me to open a browser and get it for you? [y/n] ')
    import webbrowser
    if getData.lower() == 'y':
        print 'Place it in the same directory.'
        webbrowser.open('http://cloud.github.com/downloads/kallepersson/subterranean-ng/data.zip')
    exit('')

from Game import Game
Game = Game(sys.argv)