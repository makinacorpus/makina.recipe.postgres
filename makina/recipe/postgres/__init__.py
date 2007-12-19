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
import logging
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
          - cmds : list of psql cmd to execute after all those init
        
        """
        self.buildout, self.name, self.options = buildout, name, options
        options['location'] = options['prefix'] = os.path.join(
            buildout['buildout']['parts-directory'],
            name)

    def install(self):
        """installer"""
        already_installed = False
        err_path = os.path.join(self.options['location'], 'errors.log')
        out_path = os.path.join(self.options['location'], 'cmds.log')
        if not os.path.exists(self.options['location']):
            os.mkdir(self.options['location'])
        error_occured = False
        error = None
        def system(cmd):
            code = os.system(cmd)
            if code:
                error_occured = True
                raise RuntimeError('Error running command: %s' % cmd)
        logger = logging.getLogger(self.name)
        pgdata = self.options['pgdata']
        pgdata_exists = os.path.exists(pgdata) 
            
        bin = self.options.get('bin','')
        #TODO: manage path in a better way to handle PATH case
        initdb = self.options.get('initdb',None)
        if initdb and not pgdata_exists:
            system('%s/initdb %s' % (bin, initdb) )
        
        port = self.options.get('port',None)
        if port:
            logger.warning( " !!!!!!!!!!!! " )
            logger.warning( " Warning port is not tested at the moment" )
            logger.warning( " !!!!!!!!!!!! " )
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
        pg_ctl = '%s/pg_ctl'%(buildout_bin_path)
        script = open(pg_ctl , 'w')
        script.write(pg_ctl_script % (pgdata, bin))
        script.close()
        
        #start/restart your engine !
        PIDFILE = '%s/postmaster.pid' % pgdata
        if os.path.exists(pg_ctl) and os.path.exists(PIDFILE):
            logger.info( 'Shutting down PostgreSQL server...' )
            system('%s stop' % pg_ctl)
            while os.path.exists(PIDFILE):
                time.sleep(1)
        system('%s start'%(pg_ctl))
        time.sleep(4)
        
#        createusers = self.options.get('createusers',None)
#        if createusers:
#            createusers = createusers.split(os.linesep)
#            for user in createusers:
#                if not user:continue
#                try: system('%s/createuser %s' % (bin, user) )
#                except RuntimeError,e:
#                    f.write("An error has occured while adding user %s %s"%(user,os.linesep))
#                    f.write('%s'%e)
#                    f.write(os.linesep)
#        
#        createdbs = self.options.get('createdbs', None)
#        if createdbs:
#            createdbs = createdbs.split(os.linesep)
#            for db in createdbs:
#                if not db:continue
#                try: system('%s/createdb %s' % (bin, db) )
#                except RuntimeError,e:
#                    f.write("An error has occured while adding db %s %s"%(db,os.linesep))
#                    f.write('%s'%e)
#                    f.write(os.linesep)
#        
        cmds = self.options.get('cmds', None)
        if cmds:
            cmds = cmds.split(os.linesep)
            for cmd in cmds:
                if not cmd: continue
                try: system('%s/%s' % (bin, cmd))
                except RuntimeError, e:
                    pass
        dest = self.options['location']

        if error_occured:
            logger.error('One or more error has occured. Please check log file %s' % (os.path.join(self.options['location'], 'errors.log')))
            raise RuntimeError , error
        return dest

    def update(self):
        """updater"""
        pass
