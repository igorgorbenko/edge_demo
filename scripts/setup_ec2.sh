#!/bin/bash

# Установка Docker
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Создание необходимых директорий
mkdir -p mosquitto/config
mkdir -p mosquitto/data
mkdir -p mosquitto/log

# Копирование конфигурационных файлов
cp .env.ec2 .env
cp mosquitto/config/mosquitto.conf mosquitto/config/
cp mosquitto/config/passwd mosquitto/config/

# Запуск сервисов
docker-compose up -d mqtt aws 