# Multi-Model Setup: DeepSeek + Qwen2.5-Coder

**Date:** November 29, 2024  
**Server:** instance-hulyaekiz (161.118.171.201)  
**Status:** ✅ COMPLETED

## Overview

The AI Coding Platform now supports multiple AI models for different use cases:
1. **DeepSeek Coder V2 16B** - Powerful, comprehensive code generation
2. **Qwen2.5-Coder 7B** - Fast, efficient for quick tasks

## Installed Models

### Current Models on Server

```bash
NAME                     ID              SIZE      MODIFIED
qwen2.5-coder:7b         dae161e27b0e    4.7 GB    Recently installed
deepseek-coder-v2:16b    63fb193b3a9b    8.9 GB    Primary model
```

**Total Storage Used:** ~13.6 GB

## Model Comparison

### DeepSeek Coder V2 16B
- **Size:** 8.9 GB
- **Parameters:** 16 billion
- **Best For:**
  - Complex code generation
  - Large refactoring tasks
  - Architectural decisions
  - Multi-file projects
- **Speed:** Slower but more comprehensive
- **Memory:** ~16GB RAM required

### Qwen2.5-Coder 7B
- **Size:** 4.7 GB
- **Parameters:** 7 billion
- **Best For:**
  - Quick code snippets
  - Simple functions
  - Code explanations
  - Fast iterations
- **Speed:** 2-3x faster than DeepSeek
- **Memory:** ~8GB RAM required

## Usage in OpenHands

### Using DeepSeek (Default)
OpenHands is currently configured to use DeepSeek by default:
```yaml
environment:
  - LLM_MODEL=ollama/deepseek-coder-v2:16b
  - LLM_BASE_URL=http://ollama:11434
```

### Switching to Qwen2.5-Coder

To use Qwen2.5-Coder instead, update the docker-compose.yml:

```yaml
environment:
  - LLM_MODEL=ollama/qwen2.5-coder:7b
  - LLM_BASE_URL=http://ollama:11434
```

Then restart OpenHands:
```bash
sudo docker-compose restart openhands
```

## Testing Models

### Test DeepSeek
```bash
sudo docker exec ollama-kogccog8g0ok80w0kgcoc4ck-112840189768 \
  ollama run deepseek-coder-v2:16b "Write a Python function to sort a list"
```

### Test Qwen2.5-Coder
```bash
sudo docker exec ollama-kogccog8g0ok80w0kgcoc4ck-112840189768 \
  ollama run qwen2.5-coder:7b "Write a Python function to sort a list"
```

## API Usage

Both models are accessible via Ollama API:

### Generate Endpoint
```bash
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5-coder:7b",
  "prompt": "Write a hello world function in Python",
  "stream": false
}'
```

### Chat Endpoint
```bash
curl http://localhost:11434/api/chat -d '{
  "model": "deepseek-coder-v2:16b",
  "messages": [
    {"role": "user", "content": "Explain async/await in JavaScript"}
  ],
  "stream": false
}'
```

## Resource Usage

### Current Server Capacity
- **Total RAM:** 23 GB
- **Available RAM:** 17 GB
- **Both models can run simultaneously** (if needed)

### Memory Usage by Model
- DeepSeek running: ~10-12 GB
- Qwen running: ~5-7 GB
- Both running: ~15-18 GB (still within capacity)

## Model Management

### List All Models
```bash
sudo docker exec ollama-kogccog8g0ok80w0kgcoc4ck-112840189768 ollama list
```

### Pull New Model
```bash
sudo docker exec ollama-kogccog8g0ok80w0kgcoc4ck-112840189768 ollama pull <model-name>
```

### Remove Model
```bash
sudo docker exec ollama-kogccog8g0ok80w0kgcoc4ck-112840189768 ollama rm <model-name>
```

### Show Model Info
```bash
sudo docker exec ollama-kogccog8g0ok80w0kgcoc4ck-112840189768 ollama show qwen2.5-coder:7b
```

## Recommended Usage Strategy

### Use DeepSeek For:
1. Building new features from scratch
2. Complex refactoring
3. Architecture design
4. Multi-file changes
5. When quality > speed

### Use Qwen2.5-Coder For:
1. Quick bug fixes
2. Simple functions
3. Code explanations
4. Documentation generation
5. When speed > complexity

## Future Enhancements

### Additional Models to Consider:
1. **CodeLlama 13B** - Meta's code model
2. **Mistral 7B** - General purpose, good at code
3. **Phi-3 Mini** - Very fast, lightweight
4. **StarCoder2** - Specialized for code completion

### Model Switching in UI
Future enhancement: Allow users to select model from OpenHands UI without restarting.

## Troubleshooting

### Model Not Loading
```bash
# Check Ollama logs
sudo docker logs ollama-kogccog8g0ok80w0kgcoc4ck-112840189768

# Restart Ollama
sudo docker restart ollama-kogccog8g0ok80w0kgcoc4ck-112840189768
```

### Out of Memory
```bash
# Check memory usage
free -h

# Stop unused containers
sudo docker stop <container-name>

# Remove unused models
sudo docker exec ollama-kogccog8g0ok80w0kgcoc4ck-112840189768 ollama rm <model-name>
```

### Slow Response
- Switch to Qwen2.5-Coder for faster responses
- Check if other containers are consuming resources
- Consider upgrading server RAM

## Installation Commands Reference

### Install Qwen2.5-Coder (Completed)
```bash
ssh -i AffexAI-Oracle-Servers/instance-hulya/ssh-key-2025-09-20.key ubuntu@161.118.171.201
sudo docker exec ollama-kogccog8g0ok80w0kgcoc4ck-112840189768 ollama pull qwen2.5-coder:7b
```

### Verify Installation
```bash
sudo docker exec ollama-kogccog8g0ok80w0kgcoc4ck-112840189768 ollama list
```

## Conclusion

The AI Coding Platform now has two powerful models:
- **DeepSeek Coder V2 16B** for comprehensive tasks
- **Qwen2.5-Coder 7B** for fast iterations

Both models are ready to use and can be switched based on the task requirements.

**Status:** ✅ Multi-model setup complete  
**Models Available:** 2  
**Total Storage:** 13.6 GB  
**Server Capacity:** Sufficient for both models
