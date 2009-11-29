import os,sys,urllib2,tarfile
print "Getting update..."
update = urllib2.urlopen('http://github.com/kallepersson/subterranean-ng/tarball/master')

archive = open('patch.tar.gz','wb')
archive.write(update.read())
print "Extracting update..."
archive.close()
tarball = tarfile.open('patch.tar.gz','r:gz')
members = tarball.getmembers()
folder = members[0].name
tarball.extractall()
print os.getcwd()
os.chdir(folder)
files = os.listdir('.')
for file in files:
	os.renames(file,'../'+file)
raw_input("Updated. Press any key to exit")
sys.exit()