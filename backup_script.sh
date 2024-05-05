#!/bin/bash

docker exec my-mariadb-container sh -c 'exec mysqldump --all-databases -uroot -p"$MYSQL_ROOT_PASSWORD" > db_backups/backup.sql'
