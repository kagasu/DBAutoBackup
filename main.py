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
        mysqlDumpCommand = 'mysqldump -h{0} -u{1} --password={2} --events {4} | gzip > {3}/{4}.gz'.format(
            config.get('db').get('host'),
            config.get('db').get('user'),
            config.get('db').get('password'),
            dirName,
            dbName
        )
        encryptCommand = 'openssl aes-256-cbc -e -in {0}/{1}.gz -out {0}/{1}.gz.enc -pass pass:{2}'.format(
            dirName,
            dbName,
            config.get('aes').get('password')
        )

        subprocess.call(mysqlDumpCommand, shell=True)
        subprocess.call(encryptCommand, shell=True)
        os.remove('{0}/{1}.gz'.format(dirName, dbName))
    
    subprocess.call('drive upload --file {0}'.format(dirName), shell=True)
    shutil.rmtree(dirName)

if __name__ == '__main__':
    main()
