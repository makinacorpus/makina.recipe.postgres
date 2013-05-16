Introduction
============

This package is a buildout recipe that initialize a database
using initdb command.

How to use
==========

EXAMPLE (postgis init)::

        parts =
            ...
            initdb

        [initdb]
        recipe = makina.recipe.postgres
        bin = ${buildout:directory}/parts/postgresql/bin
        initdb = --auth=trust --pgdata=${buildout:directory}/var/postgres
        pgdata = ${buildout:directory}/var/postgres
        port = 5433
        cmds =
            createuser -p 5433 --createdb    --no-createrole --no-superuser --login admin
            createuser -p 5433 --no-createdb --no-createrole --no-superuser --login zope
            createdb -p 5433 --owner admin --encoding LATIN9 zsig
            createlang -p 5433 plpgsql zsig
            psql -d zsig -p 5433 -f ${buildout:directory}/parts/postgis/share/lwpostgis.sql
            psql -d zsig -p 5433 -f ${buildout:directory}/parts/postgis/share/spatial_ref_sys.sql


bin option can be just a sym link from the /usr/bin (where all postgresql system binaries are) if you don't want to install postgres with buildout.

