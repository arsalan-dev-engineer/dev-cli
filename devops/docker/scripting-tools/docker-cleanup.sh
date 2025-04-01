
#!/bin/bash

# ANSI colour codes
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
BLUE="\033[0;34m"
RESET="\033[0m"

stop_docker_containers(){
    # '-e' enable escape sequences like \n or \t
    echo -e "\n=============== 1. STARTING DOCKER CLEANUP\n"

    # stop running docker containers
    echo -e "Stopping all docker containers"
    # get the list of running container ids (using `docker ps -q` to get just the container IDs)
    running_containers=$(docker ps -q)
    # if there are running containers, stop them
    if [ -n "$running_containers" ]; then
        # stop containers on their ids
        docker stop $running_containers
        echo -e "${GREEN}Stopped all running containers.${RESET}\n"
    else
        echo -e "${RED}No running containers found.${RESET}"
    fi
    # call function
    remove_stopped_containers
}

remove_stopped_containers(){
    echo -e "\n=============== 2. REMOVING STOPPED CONTAINERS\n"
    echo -e "Removing all stopped docker containers"
    # get the list of stopped container IDs (using `docker ps -aq` to get all containers, including stopped ones)
    # `-a` lists all containers, `-q` returns just container IDs
    stopped_containers=$(docker ps -aq)
    # check if there are any stopped containers
    if [ -n "$stopped_containers" ]; then
        # if there are stopped containers, remove them
        # remove containers by their ids
        docker rm $stopped_containers
        echo -e "${GREEN}Removed all stopped containers.${RESET}\n"
    else
        echo -e "${RED}No stopped containers found.${RESET}"
    fi
    # call function
    remove_unused_images
}

remove_unused_images(){
    echo -e "\n=============== 3. REMOVING UNUSED IMAGES\n"
    # get a list of unused (dangling) image IDs (images that are not tagged and not associated with any container)
    # check if there are any unused images
    unused_images=$(docker images -q -f "dangling=true")
    if [ -n "$unused_images" ]; then
        # if there are any unused images
        # remove the unused images by their ids
        docker rmi $unused_images
        echo -e "${GREEN}Removed all unused images.${RESET}\n"
    else
        echo -e "${RED}No unused images to remove.${RESET}"
    fi
    # call function
    remove_unused_volumes_and_networks
}

remove_unused_volumes_and_networks(){
    echo -e "\n=============== 4. REMOVING UNUSED VOLUMES AND NETWORKS\n"
    echo -e "Removing all unused volumes."
    # prune unused volumes and suppress confirmation prompt with `-f`
    # `grep -q "Total reclaimed space"` checks if any space was reclaimed during the pruning
    docker volume prune -f | grep -q "Total reclaimed space"

    echo "Removing all unused networks..."
    # prune unused networks and suppress confirmation prompt with `-f`
    # `grep -q "Total reclaimed space"` checks if any space was reclaimed during the pruning
    docker network prune -f | grep -q "Total reclaimed space"
    echo -e "${GREEN}Removed all unused networks.${RESET}\n"

    echo -e "${YELLOW}=============== END OF SCRIPT{YELLOW}\n"
}

# call function
stop_docker_containers

