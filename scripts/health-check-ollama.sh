#!/bin/bash
# Health check script for Ollama service
# Feature: self-hosted-ai-coding-platform
# Requirements: 8.3

set -e

OLLAMA_URL="${OLLAMA_URL:-http://localhost:11434}"
TIMEOUT=5

echo "🔍 Checking Ollama service health..."

# Check if Ollama is responding
if curl -sf --max-time $TIMEOUT "$OLLAMA_URL/api/tags" > /dev/null 2>&1; then
    echo "✅ Ollama service is healthy"
    
    # Check if models are loaded
    MODELS=$(curl -sf --max-time $TIMEOUT "$OLLAMA_URL/api/tags" | grep -o '"name"' | wc -l)
    echo "📦 Models loaded: $MODELS"
    
    if [ "$MODELS" -gt 0 ]; then
        echo "✅ Models are available"
        exit 0
    else
        echo "⚠️  Warning: No models loaded"
        exit 1
    fi
else
    echo "❌ Ollama service is not responding"
    exit 1
fi
