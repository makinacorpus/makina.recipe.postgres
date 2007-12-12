# -*- coding: utf-8 -*-
# Copyright (C)2007 'jeanmichel FRANCOIS'

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING. If not, write to the
# Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""Recipe postgres"""
import os
import time
from random import choice

pg_ctl_script = """
#!/bin/sh
PGDATA=%s %s/pg_ctl $@
"""

psql_script = """
#!/bin/sh
%s/psql $@
"""

class Recipe(object):
    """This recipe is used by zc.buildout"""

    def __init__(self, buildout, name, options):
        """options:
        
          - bin : path to bin folder that contains postgres binaries
          - port : port on wich postgres is started and listen
          - initdb : specify the argument to pass to the initdb command
          - createusers : list of args to pass to createuser. One line by user to create
          - createdb : list of args to pass to createdb cmd. One line by db
          - cmds : list of cmd to execute after all those init
        
        """
        self.buildout, self.name, self.options = buildout, name, options

    def install(self):
        """installer"""
        def system(cmd):
            if os.system(cmd):
                raise RuntimeError('Error running command: %s' % cmd)
        def generatepwd():
            """Return a password"""
            pwd = ''.join(choice(pwdchars) for i in range(12))
            passwd.append(pwd)
            return pwd
        pgdata = self.options['pgdata']
        bin = self.options.get('bin','')
        #TODO: manage path in a better way to handle PATH case
        initdb = self.options.get('initdb',None)
        if initdb:
            system('%s/initdb %s' % (bin, initdb) )
        
        port = self.options.get('port',None)
        if port:
            print " !!!!!!!!!!!! "
            print " Warniong port is not tested at the moment"
            print " !!!!!!!!!!!! "
            # Update the port setting and start up the server
            #FIXME we need to get pgdata from initdb option
            conffile = '%s/postgresql.conf' % pgdata
            f = open(conffile)
            conf = ('port = %s' % port).join(f.read().split('#port = 5432'))
            f.close()
            open(conffile, 'w').write(conf)
        
        # Need to know where is the bin directory of buildout
        buildout_bin_path = self.buildout['buildout']['bin-directory']
        # Create a wrapper script for psql user and admin
        script = open('%s/psql'%(buildout_bin_path) , 'w')
        script.write(psql_script % (bin))
        script.close()
        
        # Create a wrapper script for pg_ctl
        
        # Need to knwo where is 
        script = open('%s/pg_ctl'%(buildout_bin_path) , 'w')
        script.write(pg_ctl_script % (pgdata, bin))
        script.close()
        pg_ctl = script
        
        #start your engine !
        system('%s/pg_ctl start'%(buildout_bin_path))
        time.sleep(4)
        
        createusers = self.options.get('createusers',None)
        if createusers:
            createusers = createusers.split()
            for user in createusers:
                print "                "
                print "                "
                print "                "
                print "                "
                print "                "
                print "user to add : %s" % user
                print "                "
                print "                "
                print "                "
                print "                "
                print "                "
                system('%s/createuser %s' % (bin, user) )
        
        createdbs = self.options.get('createdbs', None)
        if createdbs:
            createdbs = createdbs.split()
            for db in createdbs:
                system('%s/createdb %s' % (db) )
        cmds = self.options.get('cmds', None)
        if cmds:
            cmds = cmds.split()
            for cmd in cmds:
                system(cmd)
        return tuple()

    def update(self):
        """updater"""
        pass

