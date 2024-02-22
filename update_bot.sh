#!/bin/bash
cd ~/hosting/
git pull origin master
sleep 5
git add .
sleep 5
git commit -m "Update bot"
sleep 5
git push origin master
sleep 5
sudo systemctl restart mydiscordbot.service