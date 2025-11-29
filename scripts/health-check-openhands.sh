#!/bin/bash
# Health check script for OpenHands service
# Feature: self-hosted-ai-coding-platform
# Requirements: 8.3

set -e

OPENHANDS_URL="${OPENHANDS_URL:-http://localhost:3000}"
TIMEOUT=5

echo "🔍 Checking OpenHands service health..."

# Check if OpenHands UI is responding
HTTP_CODE=$(curl -sf --max-time $TIMEOUT -o /dev/null -w "%{http_code}" "$OPENHANDS_URL" || echo "000")

if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "302" ]; then
    echo "✅ OpenHands UI is healthy (HTTP $HTTP_CODE)"
    
    # Check if container is running
    if sudo docker ps --filter "name=openhands" --format "{{.Names}}" | grep -q openhands; then
        echo "✅ OpenHands container is running"
        exit 0
    else
        echo "⚠️  Warning: OpenHands container not found"
        exit 1
    fi
else
    echo "❌ OpenHands UI is not responding (HTTP $HTTP_CODE)"
    exit 1
fi
