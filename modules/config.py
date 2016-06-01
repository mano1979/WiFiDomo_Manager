import os
import ConfigParser

config = ConfigParser.RawConfigParser()
env = os.environ.get('ENVIRONMENT', 'wifidomo')
inifile = 'etc/'+env+'.ini'
if not os.path.isfile(inifile):
    print 'Config file not found:', inifile
    exit(1)
config.read(inifile)