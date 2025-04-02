#!/bin/bash

# Define colors for better output visibility
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[0;33m"
RESET="\033[0m"

# Define the directories to check with relative paths from the root
directories=("../" "../devops/ansible" "../devops/docker" "../devops/kubernetes" "../devops/python" "../devops/terraform" "../scripting-tools")

# Checking files section (grouped together with only one space after each check)
for dir in "${directories[@]}"; do
    echo -e "${YELLOW}Checking files in the '$dir' directory...${RESET}"
done

# Space before fixing permissions (only one space here)
echo -e ""

# Loop over the directories and fix permissions
for dir in "${directories[@]}"; do
    # Ensure the directory exists before running the find command
    if [ -d "$dir" ]; then
        # Find all .sh files and loop through them
        find "$dir" -type f -name "*.sh" | while read -r file; do
            echo -e "${GREEN}Fixing permissions for: $file${RESET}"
            
            # Check if the file is executable, if not, make it executable
            if [[ ! -x "$file" ]]; then
                chmod +x "$file"
                echo -e "${GREEN}Permissions set to executable for: $file${RESET}"
            else
                echo -e "${YELLOW}File $file is already executable${RESET}"
            fi
        done
    else
        echo -e "${RED}Directory '$dir' not found, skipping...${RESET}"
    fi
done

# Space before completion message
echo -e "\n${GREEN}Permission fixing completed!${RESET}"
