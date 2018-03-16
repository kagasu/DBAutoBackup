# DBAutoBackup
Backup your MySQL(MariaDB) to Google Drive automatically

### Requirements
- gdrive  
https://github.com/prasmussen/gdrive

### Set up
1. Initialize gdrive
```sh
$ gdrive
Go to the following link in your browser: https://accounts.google.com/o/oauth2/auth?client_id=...

Enter verification code:
```
2. Edit config.json  
```sh
$ vim config.json
```

3. Change permission
```
$ chmod 777 /path/to/DBAutoBackup -R
```

4. Add cron
```sh
$ crontab -e

# DBAutoBackup(Everyday PM 16:00)
0 16 * * * /path/to/DBAutoBackup/start.sh 1> /dev/null 2> /dev/null
```

### How to decrypt
```sh
$ openssl aes-256-cbc -d -in my_db.gz.enc -out my_db.gz -pass pass:09c9ea1ca79842da94df882d20887bb6
```

# FAQ
- what is "period" ?  
old backup file delete period.  
default is 14 days.
