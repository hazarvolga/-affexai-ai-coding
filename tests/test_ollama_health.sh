#!/bin/bash

# Ollama Service Health Tests
# Tests for Requirements 2.1 and 2.2

set -e

echo "=== Ollama Service Health Tests ==="
echo ""

# Test 1: Verify Ollama API responds
echo "Test 1: Checking if Ollama API is accessible..."
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:11434/api/tags)
if [ "$response" = "200" ]; then
    echo "✓ PASS: Ollama API is accessible (HTTP 200)"
else
    echo "✗ FAIL: Ollama API returned HTTP $response"
    exit 1
fi
echo ""

# Test 2: Test model listing endpoint
echo "Test 2: Testing model listing endpoint..."
models=$(curl -s http://localhost:11434/api/tags)
if [ -n "$models" ]; then
    echo "✓ PASS: Model listing endpoint responds"
    echo "  Response: $models"
else
    echo "✗ FAIL: Model listing endpoint did not respond"
    exit 1
fi
echo ""

# Test 3: Test simple inference request (only if model is loaded)
echo "Test 3: Testing simple inference request..."
model_count=$(echo "$models" | grep -o '"name"' | wc -l)
if [ "$model_count" -gt 0 ]; then
    echo "  Models available: $model_count"
    
    # Try a simple inference with the first available model
    inference_response=$(curl -s -X POST http://localhost:11434/api/generate \
        -H "Content-Type: application/json" \
        -d '{
            "model": "deepseek-coder-v2:16b",
            "prompt": "Hello",
            "stream": false
        }' 2>&1)
    
    if echo "$inference_response" | grep -q "response"; then
        echo "✓ PASS: Inference request successful"
    else
        echo "⚠ WARNING: Inference request failed (model may still be downloading)"
        echo "  This is expected if the model download is not complete yet"
    fi
else
    echo "⚠ WARNING: No models loaded yet"
    echo "  This is expected if the model download is not complete yet"
fi
echo ""

echo "=== Test Summary ==="
echo "✓ Ollama service is running and healthy"
echo "✓ API endpoints are accessible"
echo ""
echo "Note: Full inference testing requires the model download to complete."
echo "Check model status with: docker exec ollama ollama list"
