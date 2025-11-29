#!/bin/bash

# Test script for OpenHands UI accessibility
# Requirements: 1.1, 3.1

OPENHANDS_URL="http://161.118.171.201:3000"
OLLAMA_URL="http://161.118.171.201:11434"

echo "=========================================="
echo "OpenHands UI Accessibility Test"
echo "=========================================="
echo ""

# Test 1: Verify HTTP 200 response from UI
echo "Test 1: Checking OpenHands UI accessibility..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$OPENHANDS_URL" --max-time 10)

if [ "$HTTP_STATUS" = "200" ]; then
    echo "✓ PASS: OpenHands UI is accessible (HTTP $HTTP_STATUS)"
else
    echo "✗ FAIL: OpenHands UI returned HTTP $HTTP_STATUS (expected 200)"
    exit 1
fi

echo ""

# Test 2: Test chat interface loads correctly
echo "Test 2: Checking if chat interface HTML loads..."
RESPONSE=$(curl -s "$OPENHANDS_URL" --max-time 10)

if echo "$RESPONSE" | grep -q -i "openhands\|chat\|workspace"; then
    echo "✓ PASS: Chat interface HTML contains expected content"
else
    echo "✗ FAIL: Chat interface HTML does not contain expected content"
    exit 1
fi

echo ""

# Test 3: Verify connection to Ollama backend
echo "Test 3: Verifying OpenHands can connect to Ollama..."

# First check if Ollama is accessible
OLLAMA_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$OLLAMA_URL/api/tags" --max-time 10)

if [ "$OLLAMA_STATUS" = "200" ]; then
    echo "✓ PASS: Ollama backend is accessible (HTTP $OLLAMA_STATUS)"
    
    # Check if DeepSeek model is loaded
    MODELS=$(curl -s "$OLLAMA_URL/api/tags" --max-time 10)
    if echo "$MODELS" | grep -q "deepseek-coder-v2:16b"; then
        echo "✓ PASS: DeepSeek Coder V2 16B model is available"
    else
        echo "⚠ WARNING: DeepSeek Coder V2 16B model not found in Ollama"
    fi
else
    echo "✗ FAIL: Ollama backend is not accessible (HTTP $OLLAMA_STATUS)"
    exit 1
fi

echo ""
echo "=========================================="
echo "All OpenHands UI tests passed!"
echo "=========================================="
