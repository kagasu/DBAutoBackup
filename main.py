#!/usr/bin/env python3
# coding: utf-8

import json
import MySQLdb
import subprocess
import os
import shutil
import datetime
import time
from collections import namedtuple

def GetDatabaseNames(config):
    conn = MySQLdb.connect(user = config.get('db').get('user'), password = config.get('db').get('password'), host = config.get('db').get('host'), charset = 'utf8')
    cursor = conn.cursor()

    sql = 'show databases'
    cursor.execute(sql)
    dbNames = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return [x[0] for x in dbNames if x[0] not in config.get('exclue_db_names')]

def GetGdriveDirectories():
    FileInfo = namedtuple('FileInfo', ('fileId', 'fileName', 'fileCreatedTime'))
    command = 'gdrive list --order "createdTime asc" -m 100'
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while True:
        line = proc.stdout.readline()
        if line:
            line = line.decode('utf-8').strip().split()
            fileType = line[2]
            if fileType == 'dir':
                yield FileInfo(fileId = line[0], fileName = line[1], fileCreatedTime = line[3])
        if not line and proc.poll() is not None:
            break

def DeleteOldBackup(period):
    time = datetime.datetime.now() - datetime.timedelta(days=period)
    for file in GetGdriveDirectories():
        fileCreatedTime = datetime.datetime.strptime(file.fileCreatedTime, '%Y-%m-%d')
        if time > fileCreatedTime:
            subprocess.call('gdrive delete {0} -r'.format(file.fileId), shell=True)

def main():
    config = json.load(open('config.json'))
    dbNames = GetDatabaseNames(config)

    dirName = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
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

    subprocess.call('gdrive upload {0} -r'.format(dirName), shell=True)
    time.sleep(1) # 1sec
    shutil.rmtree(dirName)

    DeleteOldBackup(config.get('gdrive').get('period'))

if __name__ == '__main__':
    main()
