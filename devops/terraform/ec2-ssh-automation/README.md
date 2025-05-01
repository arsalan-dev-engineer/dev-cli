
# AWS VPC Setup with EC2 Instance

This project challenge is part of the learning path on [roadmap.sh](https://roadmap.sh/projects/ssh-remote-server-setup).

## Project Overview

This Terraform configuration defines the following AWS resources:
- **VPC**: A Virtual Private Cloud with a CIDR block `192.168.0.0/24`.
- **Subnet**: A public subnet with a CIDR block `192.168.0.0/26`.
- **Internet Gateway (IGW)**: An IGW is attached to the VPC for internet access.
- **Route Table**: Routes traffic from the subnet to the IGW, allowing access to/from the internet.
- **Security Group**: A security group allowing inbound SSH (port 22) traffic from any IP address (can be restricted to specific IPs for production).
- **EC2 Instance**: A t2.micro EC2 instance with a public IP, accessible via SSH.

## Resources Used

- **aws_vpc**: A virtual network environment for your resources.
- **aws_subnet**: Defines a subnet within the VPC.
- **aws_internet_gateway**: Enables communication between your VPC and the internet.
- **aws_route_table**: Contains routes to direct traffic to the internet gateway.
- **aws_security_group**: Controls inbound and outbound traffic to/from the EC2 instance.
- **aws_instance**: A public EC2 instance for SSH access.

## Prerequisites

- Terraform installed onto your Linux device.
- AWS account with necessary permissions to create VPC, EC2, Security Groups, and Internet Gateway
- AWS CLI installed and configured with credentials (`aws configure`)

## Setup Instructions

#### This project is developed and managed using WSL (Windows Subsystem for Linux) with an Ubuntu environment
1. Clone the repository:
   ```bash
   https://github.com/arsalan-dev-engineer/dev-cli/tree/main/devops/terraform/ec2-ssh-automation
   ```

2. CD into the sub-directory:
    ```bash
   cd dev-cli && cd devops && cd terraform && cd ec2-ssh-automation
    ```
