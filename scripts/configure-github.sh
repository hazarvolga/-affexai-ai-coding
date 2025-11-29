#!/bin/bash

# GitHub Configuration Script for AI Coding Platform
# This script helps configure and verify GitHub integration

set -e

echo "================================================"
echo "GitHub Integration Configuration"
echo "================================================"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo ""
    echo "📝 Please edit .env file and add your GitHub token:"
    echo "   GITHUB_TOKEN=ghp_your_token_here"
    echo ""
    echo "For instructions on creating a token, see: docs/GITHUB_SETUP.md"
    exit 1
fi

# Check if GITHUB_TOKEN is set in .env
if ! grep -q "^GITHUB_TOKEN=" .env; then
    echo "❌ GITHUB_TOKEN not found in .env file"
    echo ""
    echo "Please add your GitHub token to .env file:"
    echo "   GITHUB_TOKEN=ghp_your_token_here"
    echo ""
    echo "For instructions, see: docs/GITHUB_SETUP.md"
    exit 1
fi

# Extract token from .env
GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" .env | cut -d '=' -f2)

# Check if token is still the placeholder
if [ "$GITHUB_TOKEN" = "your_github_token_here" ] || [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ GitHub token not configured"
    echo ""
    echo "Please replace 'your_github_token_here' in .env with your actual token"
    echo ""
    echo "To create a token:"
    echo "1. Visit: https://github.com/settings/tokens/new"
    echo "2. Select scopes: repo, workflow"
    echo "3. Generate and copy the token"
    echo "4. Update .env file with the token"
    echo ""
    echo "For detailed instructions, see: docs/GITHUB_SETUP.md"
    exit 1
fi

echo "✅ GitHub token found in .env file"
echo ""

# Verify token format
if [[ ! "$GITHUB_TOKEN" =~ ^(ghp_|github_pat_)[A-Za-z0-9_]+ ]]; then
    echo "⚠️  Warning: Token format looks unusual"
    echo "   Expected format: ghp_xxxx or github_pat_xxxx"
    echo "   Found: ${GITHUB_TOKEN:0:10}..."
    echo ""
fi

# Test token with GitHub API
echo "🔍 Testing GitHub token..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "Authorization: token $GITHUB_TOKEN" \
    https://api.github.com/user)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ GitHub token is valid!"
    
    # Get user info
    USER_INFO=$(curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user)
    USERNAME=$(echo "$USER_INFO" | grep -o '"login": *"[^"]*"' | cut -d'"' -f4)
    
    if [ -n "$USERNAME" ]; then
        echo "   Authenticated as: $USERNAME"
    fi
    echo ""
elif [ "$HTTP_CODE" = "401" ]; then
    echo "❌ GitHub token is invalid or expired"
    echo ""
    echo "Please generate a new token:"
    echo "1. Visit: https://github.com/settings/tokens"
    echo "2. Delete the old token"
    echo "3. Create a new token with 'repo' and 'workflow' scopes"
    echo "4. Update .env file with the new token"
    echo ""
    exit 1
else
    echo "⚠️  Warning: Unable to verify token (HTTP $HTTP_CODE)"
    echo "   This might be a network issue"
    echo ""
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running"
    echo "   Please start Docker and try again"
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Check if containers are running
if docker ps | grep -q "openhands"; then
    echo "🔄 OpenHands container is running"
    echo "   Restarting to apply GitHub token..."
    echo ""
    
    docker-compose restart openhands
    
    echo ""
    echo "✅ OpenHands restarted successfully"
else
    echo "🚀 Starting services..."
    echo ""
    
    docker-compose up -d
    
    echo ""
    echo "✅ Services started successfully"
fi

echo ""
echo "================================================"
echo "Configuration Complete!"
echo "================================================"
echo ""
echo "GitHub integration is now configured."
echo ""
echo "Next steps:"
echo "1. Access OpenHands at: http://localhost:3000"
echo "2. Test GitHub integration by asking the AI to:"
echo "   - Create a new project"
echo "   - Initialize a Git repository"
echo "   - Push to GitHub"
echo ""
echo "For troubleshooting, see: docs/GITHUB_SETUP.md"
echo ""
