#!/bin/bash


apt update && apt install -y apt-transport-https ca-certificates curl software-properties-common git

curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker.asc] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

apt update
apt-cache policy docker-ce
apt install docker-ce

systemctl start docker
systemctl enable docker

curl -L "https://github.com/docker/compose/releases/download/2.25.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

git clone https://github.com/JohanHelm/SibGMU_TZ.git $(HOME)/TZ_SibGMU

cd $(HOME)/TZ_SibGMU

chmod +x $(HOME)/TZ_SibGMU/backup_script.sh

echo "*/5 * * * * $(HOME)/TZ_SibGMU/backup_script.sh" | crontab -
crontab -l

docker-compose build
docker-compose up --force-recreate -d


