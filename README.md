# DevOps Projects & Automation Tools
This repository contains a variety of DevOps projects, automation scripts, and tools designed to streamline infrastructure, cloud management, and other automation tasks.

## Getting Started
To get started with the project, follow these steps:  
1. **Set permissions for fix-permissions.sh**  
   Make the script executable by running:
   
   ```bash
   chmod +x scripting-tools/fix-permissions.sh
   ```

3. **Run fix-permissions.sh:**  
   Execute the script to set up file permissions:

   ```bash
   ./scripting-tools/fix-permissions.sh
   ```

4. **Run setup.sh:**  
   Install dependencies and configure the project by running:

   ```bash
   ./setup.sh
   ```

## commands/
This folder contains Python scripts categorised by functionality:
* **AWS**: Automation scripts for managing AWS resources such as EC2 and S3.
* **Docker**: Contains scripts for Docker cleanup and management.
* **Toolkit**: Includes utility scripts for general purpose tasks like cache management.

## dev_cli/
The directory contains the dev_cli.py script, which serves as the main entry point for the CLI tool.  
It uses Click to organise and run DevOps-related automation commands under a common command group.

## scripting-tools/
Contains utility scripts for system and DevOps automation.

## devops/
**terraform/**
1. **ec2-ssh-automation**  
   This project challenge is part of the learning path on [roadmap.sh](https://roadmap.sh/projects/ssh-remote-server-setup).
   To access this project, run the following command:

   ```bash
   cd devops && cd terraform && cd ec2-ssh-automation
   ```
