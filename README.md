# AffexAI AI Coding Platform

A self-hosted AI coding platform running on Oracle Cloud, providing a Vibe Coding-like experience using open-source tools. Build applications with AI assistance, version control with GitHub, and deploy with Coolify - all without external API costs.

## 🚀 Quick Start

**Access the platform:**
- **OpenHands UI**: https://ai.fpvlovers.com.tr
- **Coolify Dashboard**: https://coolify.fpvlovers.com.tr

**First time setup:**
1. Access OpenHands at the URL above
2. Start chatting with the AI to build your application
3. (Optional) Configure GitHub integration for version control

## 📦 Services

- **Ollama**: Local AI model inference engine
  - DeepSeek Coder V2 16B (primary model - comprehensive, best for complex tasks)
  - Qwen2.5-Coder 7B (secondary model - fast, efficient for simple tasks)
- **OpenHands**: Web-based autonomous AI coding assistant
- **Coolify**: Self-hosted deployment and management platform

## ✨ Features

- 🤖 **AI-Powered Coding**: Chat with AI to generate, modify, and debug code
- 🔒 **100% Self-Hosted**: All AI processing runs locally, no external API costs
- 🌐 **Web-Based**: Access from any browser, no local installation required
- 🔐 **Secure**: HTTPS enabled, GitHub token encryption, firewall configured
- 📦 **GitHub Integration**: Automatic repository creation, commits, and pushes
- 🚀 **One-Click Deploy**: Deploy applications directly through Coolify
- 💾 **Persistent Workspace**: All projects saved and accessible
- 🔄 **Auto-Restart**: Services automatically recover from failures

## 🛠️ Prerequisites

- Docker and Docker Compose installed
- Docker network `ai-coding-network` created
- Minimum 30GB disk space available
- 16GB RAM recommended for optimal performance
- Oracle Cloud instance (or any Linux server)

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

### GitHub Integration (Optional)

To enable GitHub integration for repository operations:

1. **Create a GitHub Personal Access Token**
   - Follow the detailed guide: [docs/GITHUB_SETUP.md](docs/GITHUB_SETUP.md)
   - Required permissions: `repo`, `workflow`

2. **Configure the Token**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your token
   GITHUB_TOKEN=ghp_your_token_here
   ```

3. **Apply Configuration (Automated)**
   ```bash
   # Run the configuration script (verifies token and restarts services)
   bash scripts/configure-github.sh
   ```

   Or manually restart services:
   ```bash
   docker-compose restart openhands
   ```

For complete setup instructions, see [GitHub Integration Setup Guide](docs/GITHUB_SETUP.md).

### Environment Variables

- `GITHUB_TOKEN`: GitHub personal access token for repository operations (optional)
  - **Required permissions**: `repo`, `workflow`
  - **Setup guide**: [docs/GITHUB_SETUP.md](docs/GITHUB_SETUP.md)
- `LLM_MODEL`: AI model to use
  - `ollama/deepseek-coder-v2:16b` (default - comprehensive, slower)
  - `ollama/qwen2.5-coder:7b` (alternative - fast, efficient)
  - **See**: [docs/MULTI_MODEL_SETUP.md](docs/MULTI_MODEL_SETUP.md) for model comparison
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
│   Workspace     │      │  AI Models   │
│   /opt/workspace│      │ DeepSeek 16B │
│   ├── projects/ │      │ Qwen2.5 7B   │
│   └── temp/     │      └──────────────┘
└─────────────────┘
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

## 📚 Documentation

- **[GitHub Integration Setup](docs/GITHUB_SETUP.md)**: Configure GitHub for version control
- **[Multi-Model Setup](docs/MULTI_MODEL_SETUP.md)**: Switch between AI models
- **[Secrets Management](docs/SECRETS_MANAGEMENT.md)**: Secure credential handling
- **[Firewall Configuration](docs/FIREWALL_CONFIGURATION.md)**: Network security setup
- **[Deployment Status](docs/DEPLOYMENT_STATUS.md)**: Current deployment information

## 🔧 Troubleshooting

### OpenHands not responding
```bash
# Check if container is running
sudo docker ps | grep openhands

# View logs
sudo docker logs openhands-<container-id>

# Restart service via Coolify UI or:
sudo docker restart openhands-<container-id>
```

### Ollama model not loading
```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# View available models
sudo docker exec ollama-<container-id> ollama list

# Pull model if missing
sudo docker exec ollama-<container-id> ollama pull deepseek-coder-v2:16b
```

### GitHub authentication failed
```bash
# Verify token is set in Coolify environment variables
# Or check .env file on server
cat ~/.env | grep GITHUB_TOKEN

# Test token validity
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
```

### System health check
```bash
# Run comprehensive health check
bash ~/health-check-system.sh
```

## 🔍 Monitoring

### Health Check Scripts
```bash
# Check Ollama service
bash scripts/health-check-ollama.sh

# Check OpenHands service
bash scripts/health-check-openhands.sh

# Check entire system
bash scripts/health-check-system.sh
```

### View Logs
```bash
# OpenHands logs
sudo docker logs -f openhands-<container-id>

# Ollama logs
sudo docker logs -f ollama-<container-id>

# All services
sudo docker ps --format "table {{.Names}}\t{{.Status}}"
```

### Resource Usage
```bash
# Check disk space
df -h

# Check memory usage
free -h

# Check Docker resource usage
sudo docker stats
```

## 🔐 Security

- **HTTPS**: All web interfaces use SSL/TLS encryption
- **Firewall**: Only necessary ports exposed (80, 443, 8000)
- **Secrets**: GitHub tokens stored securely in environment variables
- **Network Isolation**: Internal services not directly accessible
- **Auto-Updates**: Coolify manages service updates

## 🤝 Contributing

This is a private deployment for AffexAI. For issues or improvements:
1. Document the issue in the project repository
2. Test changes in a development environment
3. Update relevant documentation
4. Deploy via Coolify

## 📝 License

Private deployment for AffexAI internal use.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section above
2. Review logs for error messages
3. Consult the documentation in `/docs`
4. Contact the system administrator

---

**Instance Details:**
- **Server**: instance-hulyaekiz (Oracle Cloud)
- **IP**: 161.118.171.201
- **Deployed**: November 2025
- **Status**: ✅ Production
