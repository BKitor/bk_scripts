#!/usr/bin/bash

/usr/bin/rsync -av -L /home/bkitor/Documents bkitor@192.168.1.17:/home/bkitor/X1_backup/daily
/usr/bin/rsync -av -L /home/bkitor/Research bkitor@192.168.1.17:/home/bkitor/X1_backup/daily
echo $(date) > /home/bkitor/bk_backup.log
/usr/bin/rsync -av /home/bkitor/bk_backup.log bkitor@192.168.1.17:/home/bkitor/X1_backup/daily