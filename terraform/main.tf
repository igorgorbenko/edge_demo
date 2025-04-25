terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-central-1"  # Франкфурт
}

# VPC и сетевая инфраструктура
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "mqtt-vpc"
  }
}

resource "aws_subnet" "main" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "eu-central-1a"
  map_public_ip_on_launch = true

  tags = {
    Name = "mqtt-subnet"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "mqtt-igw"
  }
}

resource "aws_route_table" "main" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "mqtt-route-table"
  }
}

resource "aws_route_table_association" "main" {
  subnet_id      = aws_subnet.main.id
  route_table_id = aws_route_table.main.id
}

# Security Group
resource "aws_security_group" "mqtt" {
  name        = "mqtt-security-group"
  description = "Security group for MQTT broker"
  vpc_id      = aws_vpc.main.id

  # SSH доступ
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # В продакшене лучше ограничить конкретными IP
  }

  # MQTT порт
  ingress {
    from_port   = 1883
    to_port     = 1883
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # В продакшене лучше ограничить конкретными IP
  }

  # Исходящий трафик
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "mqtt-security-group"
  }
}

# EC2 Instance
resource "aws_instance" "mqtt" {
  ami           = "ami-0669b163befffbdfc"  # Amazon Linux 2023 AMI для eu-central-1
  instance_type = "t2.medium"
  subnet_id     = aws_subnet.main.id

  vpc_security_group_ids = [aws_security_group.mqtt.id]
  key_name              = aws_key_pair.mqtt.key_name

  root_block_device {
    volume_size = 30  # GB
    volume_type = "gp3"
  }

  tags = {
    Name = "mqtt-broker"
  }

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y docker
              systemctl start docker
              systemctl enable docker
              usermod -a -G docker ec2-user
              curl -L "https://github.com/docker/compose/releases/download/v2.24.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
              chmod +x /usr/local/bin/docker-compose
              EOF
}

# SSH Key Pair
resource "aws_key_pair" "mqtt" {
  key_name   = "mqtt-key"
  public_key = file("${path.module}/ssh/mqtt.pub")  # Укажите путь к вашему публичному ключу
}

# Outputs
output "public_ip" {
  value = aws_instance.mqtt.public_ip
}

output "public_dns" {
  value = aws_instance.mqtt.public_dns
} 