#!/usr/bin/env python3
# coding: utf-8

import json
import MySQLdb
import subprocess
import os
import shutil
from datetime import datetime as dt

def GetDatabaseNames(config):
    conn = MySQLdb.connect(user = config.get('db').get('user'), password = config.get('db').get('password'), host = config.get('db').get('host'), charset = 'utf8')
    cursor = conn.cursor()

    sql = 'show databases'
    cursor.execute(sql)
    dbNames = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return [x[0] for x in dbNames if x[0] not in config.get('exclue_db_names')]

def main():
    config = json.load(open('config.json'))
    dbNames = GetDatabaseNames(config)

    dirName = dt.now().strftime('%Y%m%d_%H%M%S')
    os.mkdir(dirName)

    for dbName in dbNames:
        mysqlDumpCommand = 'mysqldump -h{0} -u{1} --password={2} --events {3} | gzip > {4}/{3}.gz'.format(
            config.get('db').get('host'),
            config.get('db').get('user'),
            config.get('db').get('password'),
            dbName,
            dirName
        )
        subprocess.call(mysqlDumpCommand, shell=True)
    
    subprocess.call('drive upload --file {0}'.format(dirName), shell=True)
    shutil.rmtree(dirName)

if __name__ == '__main__':
    main()
