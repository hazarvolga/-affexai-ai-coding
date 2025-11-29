#!/bin/bash
# Setup workspace directory structure for OpenHands
# This script creates the required directory structure inside the Docker volume
# 
# NOTE: This project runs on Oracle Cloud via Coolify
# Server: instance-hulyaekiz (161.118.171.201)
# Coolify Dashboard: https://coolify.fpvlovers.com.tr

set -e

echo "Setting up workspace directory structure..."
echo "NOTE: Running on Oracle Cloud instance via Coolify"

# Define workspace base directory
WORKSPACE_BASE="/opt/workspace"

# Check if we're running inside the container or need to use docker exec
if [ -d "$WORKSPACE_BASE" ]; then
    # Running inside container
    echo "Running inside container, setting up directories directly..."
    
    # Create projects directory
    mkdir -p "$WORKSPACE_BASE/projects"
    echo "✓ Created $WORKSPACE_BASE/projects"
    
    # Create temp directory
    mkdir -p "$WORKSPACE_BASE/temp"
    echo "✓ Created $WORKSPACE_BASE/temp"
    
    # Set appropriate permissions (readable/writable by all users in container)
    chmod 755 "$WORKSPACE_BASE/projects"
    chmod 755 "$WORKSPACE_BASE/temp"
    echo "✓ Set permissions on directories"
    
    echo "Workspace structure created successfully!"
    ls -la "$WORKSPACE_BASE"
else
    # Running on host, need to use docker exec
    echo "Running on Oracle Cloud host, using docker exec to setup directories..."
    
    CONTAINER_NAME="openhands"
    
    # Check if container is running
    if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        echo "Error: Container '$CONTAINER_NAME' is not running"
        echo "Please start the container first with: docker-compose up -d"
        echo "Or check Coolify dashboard at: https://coolify.fpvlovers.com.tr"
        exit 1
    fi
    
    # Create directories inside container
    docker exec "$CONTAINER_NAME" mkdir -p "$WORKSPACE_BASE/projects"
    echo "✓ Created $WORKSPACE_BASE/projects"
    
    docker exec "$CONTAINER_NAME" mkdir -p "$WORKSPACE_BASE/temp"
    echo "✓ Created $WORKSPACE_BASE/temp"
    
    # Set appropriate permissions
    docker exec "$CONTAINER_NAME" chmod 755 "$WORKSPACE_BASE/projects"
    docker exec "$CONTAINER_NAME" chmod 755 "$WORKSPACE_BASE/temp"
    echo "✓ Set permissions on directories"
    
    echo "Workspace structure created successfully!"
    docker exec "$CONTAINER_NAME" ls -la "$WORKSPACE_BASE"
fi

echo ""
echo "Workspace directory structure:"
echo "  $WORKSPACE_BASE/"
echo "  ├── projects/  (for user projects)"
echo "  └── temp/      (for temporary files)"
echo ""
echo "To run this on Oracle Cloud server:"
echo "  ssh ubuntu@161.118.171.201"
echo "  cd /path/to/project"
echo "  ./scripts/setup-workspace.sh"
