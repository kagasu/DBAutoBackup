# DBAutoBackup
Backup your MySQL(MariaDB) to Google Drive automatically

# Requirements
- gdrive  
https://github.com/prasmussen/gdrive

# How to decrypt
```sh
openssl aes-256-cbc -d -in my_db.gz.enc -out my_db.gz -pass pass:09c9ea1ca79842da94df882d20887bb6
```
