#!/bin/bash
# Prerequisites Verification Script for AI Coding Platform
# Instance: instance-hulyaekiz (161.118.171.201)

echo "==================================="
echo "AI Coding Platform Prerequisites"
echo "==================================="
echo ""

# Check Docker
echo "1. Checking Docker installation..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    echo "   ✓ Docker is installed: $DOCKER_VERSION"
else
    echo "   ✗ Docker is NOT installed"
    exit 1
fi
echo ""

# Check disk space
echo "2. Checking available disk space (minimum 30GB required)..."
AVAILABLE_SPACE=$(df -h / | awk 'NR==2 {print $4}')
AVAILABLE_GB=$(df / | awk 'NR==2 {print $4}')
if [ "$AVAILABLE_GB" -gt 30000000 ]; then
    echo "   ✓ Sufficient disk space available: $AVAILABLE_SPACE"
else
    echo "   ✗ Insufficient disk space: $AVAILABLE_SPACE (minimum 30GB required)"
    exit 1
fi
echo ""

# Check Docker Compose
echo "3. Checking Docker Compose installation..."
if docker compose version &> /dev/null; then
    COMPOSE_VERSION=$(docker compose version)
    echo "   ✓ Docker Compose is installed: $COMPOSE_VERSION"
else
    echo "   ✗ Docker Compose is NOT installed"
    exit 1
fi
echo ""

# Check ai-coding-network
echo "4. Checking ai-coding-network existence..."
if sudo docker network ls | grep -q "ai-coding-network"; then
    echo "   ✓ ai-coding-network exists"
    sudo docker network inspect ai-coding-network | grep -A 5 "IPAM"
else
    echo "   ✗ ai-coding-network does NOT exist"
    echo "   Creating ai-coding-network..."
    sudo docker network create ai-coding-network
    if [ $? -eq 0 ]; then
        echo "   ✓ ai-coding-network created successfully"
    else
        echo "   ✗ Failed to create ai-coding-network"
        exit 1
    fi
fi
echo ""

echo "==================================="
echo "All prerequisites verified!"
echo "==================================="
echo ""
echo "Summary:"
echo "  - Docker: Installed"
echo "  - Disk Space: $AVAILABLE_SPACE available"
echo "  - Docker Compose: Installed"
echo "  - ai-coding-network: Exists"
echo ""
echo "Instance is ready for AI Coding Platform deployment."
