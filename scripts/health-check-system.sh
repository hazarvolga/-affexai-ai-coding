#!/bin/bash
# Combined system health check script
# Feature: self-hosted-ai-coding-platform
# Requirements: 8.3

set -e

echo "🏥 AI Coding Platform - System Health Check"
echo "=========================================="
echo ""

OVERALL_STATUS=0

# Check Ollama
echo "1️⃣  Ollama Service:"
if bash "$(dirname "$0")/health-check-ollama.sh" 2>&1 | grep -v "^🔍"; then
    echo ""
else
    OVERALL_STATUS=1
    echo ""
fi

# Check OpenHands
echo "2️⃣  OpenHands Service:"
if bash "$(dirname "$0")/health-check-openhands.sh" 2>&1 | grep -v "^🔍"; then
    echo ""
else
    OVERALL_STATUS=1
    echo ""
fi

# Check disk space
echo "3️⃣  Disk Space:"
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -lt 80 ]; then
    echo "✅ Disk usage: ${DISK_USAGE}% (healthy)"
else
    echo "⚠️  Warning: Disk usage: ${DISK_USAGE}% (high)"
    OVERALL_STATUS=1
fi
echo ""

# Check memory
echo "4️⃣  Memory Usage:"
MEMORY_USAGE=$(free | awk 'NR==2 {printf "%.0f", $3/$2 * 100}')
if [ "$MEMORY_USAGE" -lt 90 ]; then
    echo "✅ Memory usage: ${MEMORY_USAGE}% (healthy)"
else
    echo "⚠️  Warning: Memory usage: ${MEMORY_USAGE}% (high)"
    OVERALL_STATUS=1
fi
echo ""

# Check Docker
echo "5️⃣  Docker Status:"
if sudo docker info > /dev/null 2>&1; then
    RUNNING_CONTAINERS=$(sudo docker ps --filter "name=openhands|ollama" --format "{{.Names}}" | wc -l)
    echo "✅ Docker is running"
    echo "📦 AI Platform containers: $RUNNING_CONTAINERS/2"
    if [ "$RUNNING_CONTAINERS" -lt 2 ]; then
        echo "⚠️  Warning: Not all containers are running"
        OVERALL_STATUS=1
    fi
else
    echo "❌ Docker is not responding"
    OVERALL_STATUS=1
fi
echo ""

# Final status
echo "=========================================="
if [ $OVERALL_STATUS -eq 0 ]; then
    echo "✅ System Status: HEALTHY"
    exit 0
else
    echo "⚠️  System Status: DEGRADED"
    exit 1
fi
