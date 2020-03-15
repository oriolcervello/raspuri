#!/bin/bash  
# Give execution rights on the cron job
#chmod 0644 dnsupdate

# Apply cron job
crontab dnsupdate


docker run --name webR --rm -p 80:80 -d -v /home/ori/OUT/plot:/usr/share/nginx/html/OUT/plot webrasp
