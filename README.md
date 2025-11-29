# AffexAI AI Coding Platform

Self-hosted AI coding platform running on Oracle Cloud with Ollama and OpenHands.

## Services

- **Ollama**: Local AI model inference (DeepSeek Coder V2 16B)
- **OpenHands**: Web-based AI coding assistant
- **Coolify**: Deployment and management platform

## Prerequisites

- Docker and Docker Compose installed
- Docker network `ai-coding-network` created
- Minimum 30GB disk space
- 16GB RAM recommended

## Deployment

### Using Coolify (Recommended)

1. Connect this repository to Coolify
2. Set environment variables in Coolify:
   - `GITHUB_TOKEN` (optional, for GitHub integration)
3. Deploy the service
4. Access OpenHands at: http://your-domain:3000

### Manual Deployment

```bash
# Create network if not exists
docker network create ai-coding-network

# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

## Configuration

### Environment Variables

- `GITHUB_TOKEN`: GitHub personal access token for repository operations (optional)
- `LLM_MODEL`: AI model to use (default: ollama/deepseek-coder-v2:16b)
- `LLM_BASE_URL`: Ollama API URL (default: http://ollama:11434)
- `WORKSPACE_DIR`: OpenHands workspace directory (default: /opt/workspace)

## Testing

Run health checks:

```bash
# Test Ollama
bash tests/test_ollama_health.sh

# Test OpenHands UI
bash tests/test_openhands_ui.sh
```

## Architecture

```
┌─────────────────┐
│   User Browser  │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐
│  Traefik Proxy  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│   OpenHands     │─────▶│   Ollama     │
│   (Port 3000)   │      │ (Port 11434) │
└─────────────────┘      └──────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐      ┌──────────────┐
│   Workspace     │      │ DeepSeek V2  │
│   /opt/workspace│      │     16B      │
└─────────────────┘      └──────────────┘
```

## Ports

- `3000`: OpenHands web interface
- `11434`: Ollama API (internal)

## Volumes

- `ollama-data`: Stores AI models
- `openhands-workspace`: Project workspace

## Network

All services run on `ai-coding-network` Docker bridge network.

## Instance Details

- **Oracle Instance**: instance-hulyaekiz
- **IP**: 161.118.171.201
- **Domain**: ai.fpvlovers.com.tr (to be configured)

## Support

For issues and questions, check the logs:

```bash
docker-compose logs ollama
docker-compose logs openhands
```
