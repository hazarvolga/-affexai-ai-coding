# Configuration Reference

## Overview
This document provides a complete reference for all configuration options in the AI Coding Platform.

## Environment Variables

### Core Configuration

#### `GITHUB_TOKEN`
- **Type**: String
- **Required**: No (optional)
- **Default**: None
- **Description**: GitHub personal access token for repository operations
- **Format**: `ghp_` followed by 36 alphanumeric characters
- **Permissions Required**: `repo`, `workflow`
- **Example**: `GITHUB_TOKEN=ghp_abc123def456...`
- **Security**: Store securely, never commit to Git
- **Documentation**: [GitHub Setup Guide](GITHUB_SETUP.md)

#### `LLM_MODEL`
- **Type**: String
- **Required**: Yes
- **Default**: `ollama/deepseek-coder-v2:16b`
- **Description**: AI model to use for code generation
- **Options**:
  - `ollama/deepseek-coder-v2:16b` - Comprehensive, best quality (slower)
  - `ollama/qwen2.5-coder:7b` - Fast, efficient (good quality)
- **Example**: `LLM_MODEL=ollama/qwen2.5-coder:7b`
- **Documentation**: [Multi-Model Setup](MULTI_MODEL_SETUP.md)

#### `LLM_BASE_URL`
- **Type**: URL
- **Required**: Yes
- **Default**: `http://ollama:11434`
- **Description**: Ollama API endpoint URL
- **Format**: `http://hostname:port`
- **Example**: `LLM_BASE_URL=http://ollama:11434`
- **Note**: Use Docker service name for internal network

#### `OLLAMA_HOST`
- **Type**: String
- **Required**: Yes
- **Default**: `http://ollama:11434`
- **Description**: Ollama service host address
- **Example**: `OLLAMA_HOST=http://ollama:11434`

#### `OLLAMA_MODEL`
- **Type**: String
- **Required**: Yes
- **Default**: `deepseek-coder-v2:16b`
- **Description**: Default model name for Ollama
- **Example**: `OLLAMA_MODEL=qwen2.5-coder:7b`

### Workspace Configuration

#### `WORKSPACE_DIR`
- **Type**: Path
- **Required**: Yes
- **Default**: `/opt/workspace`
- **Description**: Directory where OpenHands stores projects
- **Example**: `WORKSPACE_DIR=/opt/workspace`
- **Note**: Must be writable by OpenHands container

#### `OPENHANDS_WORKSPACE`
- **Type**: Path
- **Required**: Yes
- **Default**: `/opt/workspace`
- **Description**: OpenHands workspace directory path
- **Example**: `OPENHANDS_WORKSPACE=/opt/workspace`

### Domain Configuration

#### `OPENHANDS_DOMAIN`
- **Type**: Domain
- **Required**: No (for production)
- **Default**: None
- **Description**: Public domain for OpenHands UI
- **Example**: `OPENHANDS_DOMAIN=ai.fpvlovers.com.tr`
- **Note**: Configure DNS A record to point to server IP

#### `COOLIFY_DOMAIN`
- **Type**: Domain
- **Required**: No (for production)
- **Default**: None
- **Description**: Public domain for Coolify dashboard
- **Example**: `COOLIFY_DOMAIN=coolify.fpvlovers.com.tr`

### Security Configuration

#### `OPENHANDS_PASSWORD`
- **Type**: String
- **Required**: No (optional)
- **Default**: None
- **Description**: Password for basic authentication on OpenHands UI
- **Example**: `OPENHANDS_PASSWORD=secure_password_123`
- **Security**: Use strong password, store securely
- **Note**: Currently not implemented, reserved for future use

#### `LETSENCRYPT_EMAIL`
- **Type**: Email
- **Required**: No (recommended)
- **Default**: None
- **Description**: Email for Let's Encrypt certificate notifications
- **Example**: `LETSENCRYPT_EMAIL=admin@fpvlovers.com.tr`
- **Note**: Managed by Coolify/Traefik

### Coolify API Configuration

#### `COOLIFY_API_TOKEN`
- **Type**: String
- **Required**: No (optional)
- **Default**: None
- **Description**: API token for Coolify automation
- **Example**: `COOLIFY_API_TOKEN=your_coolify_token_here`
- **Documentation**: [Coolify API Docs](https://coolify.io/docs/api)

#### `COOLIFY_API_URL`
- **Type**: URL
- **Required**: No (optional)
- **Default**: None
- **Description**: Coolify API endpoint
- **Example**: `COOLIFY_API_URL=https://coolify.fpvlovers.com.tr/api`

## Docker Compose Configuration

### Services

#### Ollama Service
```yaml
ollama:
  image: ollama/ollama:latest
  container_name: ollama
  ports:
    - "11434:11434"
  volumes:
    - ollama-data:/root/.ollama
  networks:
    - ai-coding-network
  restart: unless-stopped
  environment:
    - OLLAMA_HOST=0.0.0.0:11434
```

**Configuration Options:**
- `image`: Docker image to use (default: `ollama/ollama:latest`)
- `ports`: Expose port 11434 for API access
- `volumes`: Persistent storage for models
- `restart`: Auto-restart policy
- `environment.OLLAMA_HOST`: Bind address for Ollama API

#### OpenHands Service
```yaml
openhands:
  image: ghcr.io/all-hands-ai/openhands:latest
  container_name: openhands
  ports:
    - "3000:3000"
  volumes:
    - openhands-workspace:/opt/workspace
    - /var/run/docker.sock:/var/run/docker.sock
  networks:
    - ai-coding-network
  depends_on:
    - ollama
  restart: unless-stopped
  environment:
    - LLM_MODEL=${LLM_MODEL}
    - LLM_BASE_URL=${LLM_BASE_URL}
    - WORKSPACE_DIR=${WORKSPACE_DIR}
    - GITHUB_TOKEN=${GITHUB_TOKEN}
```

**Configuration Options:**
- `image`: Docker image to use
- `ports`: Expose port 3000 for web UI
- `volumes`: Workspace storage and Docker socket access
- `depends_on`: Wait for Ollama to start
- `environment`: Pass configuration via environment variables

### Volumes

#### `ollama-data`
- **Purpose**: Store AI models and Ollama configuration
- **Location**: Docker managed volume
- **Size**: ~20GB for DeepSeek 16B model
- **Backup**: Important - contains downloaded models

#### `openhands-workspace`
- **Purpose**: Store user projects and code
- **Location**: Docker managed volume
- **Size**: Grows with projects
- **Backup**: Critical - contains all user work

### Networks

#### `ai-coding-network`
- **Type**: Bridge network
- **Purpose**: Internal communication between services
- **Subnet**: 10.0.5.0/24 (example)
- **External**: No (internal only)
- **Services**: Ollama, OpenHands, Coolify proxy

## Coolify Configuration

### Application Settings

**General:**
- **Name**: AI Coding Platform
- **Project**: affexai-ai-coding
- **Environment**: production

**Build:**
- **Build Pack**: Docker Compose
- **Docker Compose Location**: `./docker-compose.yml`
- **Base Directory**: `/`

**Domains:**
- OpenHands: `ai.fpvlovers.com.tr`
- Coolify: `coolify.fpvlovers.com.tr`

**SSL/TLS:**
- **Provider**: Let's Encrypt
- **Auto-Renew**: Enabled
- **Force HTTPS**: Enabled

**Environment Variables:**
Configure in Coolify UI under "Environment Variables" tab:
- `GITHUB_TOKEN`: (if using GitHub integration)
- `LLM_MODEL`: Model selection
- Other variables as needed

### Deployment Settings

**Auto Deploy:**
- **Enabled**: Yes (optional)
- **Branch**: main
- **Trigger**: Push to repository

**Health Checks:**
- **OpenHands**: HTTP GET to `/` expecting 200
- **Ollama**: HTTP GET to `/api/tags` expecting 200

**Restart Policy:**
- **Policy**: unless-stopped
- **Max Retries**: Unlimited
- **Restart Delay**: 10 seconds

## Network Architecture

```
Internet
   │
   ├─── Port 80 (HTTP) ──────┐
   ├─── Port 443 (HTTPS) ────┤
   └─── Port 8000 (Coolify) ─┤
                              │
                              ▼
                    ┌──────────────────┐
                    │  Traefik Proxy   │
                    │   (Coolify)      │
                    └────────┬─────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
    ┌──────────────────┐         ┌──────────────────┐
    │   OpenHands      │────────▶│     Ollama       │
    │   Port 3000      │         │   Port 11434     │
    │  (Internal)      │         │   (Internal)     │
    └──────────────────┘         └──────────────────┘
              │                             │
              ▼                             ▼
    ┌──────────────────┐         ┌──────────────────┐
    │   Workspace      │         │   AI Models      │
    │ /opt/workspace   │         │  DeepSeek 16B    │
    └──────────────────┘         │  Qwen2.5 7B      │
                                 └──────────────────┘
```

## Port Reference

| Port  | Service          | Access      | Protocol | Purpose                    |
|-------|------------------|-------------|----------|----------------------------|
| 80    | Traefik          | Public      | HTTP     | Redirect to HTTPS          |
| 443   | Traefik          | Public      | HTTPS    | Secure web access          |
| 8000  | Coolify          | Public      | HTTP     | Coolify dashboard          |
| 3000  | OpenHands        | Internal    | HTTP     | Web UI (proxied)           |
| 11434 | Ollama           | Internal    | HTTP     | AI model API               |

## File Locations

### On Server

```
/home/ubuntu/
├── .env                          # Environment variables
├── docker-compose.yml            # Service definitions (if manual)
├── health-check-*.sh             # Health check scripts
└── verify-prerequisites.sh       # Prerequisites check

/opt/workspace/
├── projects/                     # User projects
│   ├── project-1/
│   └── project-2/
└── temp/                         # Temporary files

/var/lib/docker/volumes/
├── ollama-data/                  # AI models storage
└── openhands-workspace/          # Projects storage
```

### In Repository

```
.
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
├── README.md                     # Main documentation
├── docker-compose.yml            # Service definitions
├── docs/                         # Documentation
│   ├── CONFIGURATION_REFERENCE.md
│   ├── DEPLOYMENT_STATUS.md
│   ├── FIREWALL_CONFIGURATION.md
│   ├── GITHUB_SETUP.md
│   ├── MULTI_MODEL_SETUP.md
│   └── SECRETS_MANAGEMENT.md
├── scripts/                      # Utility scripts
│   ├── configure-github.sh
│   ├── health-check-ollama.sh
│   ├── health-check-openhands.sh
│   ├── health-check-system.sh
│   └── setup-workspace.sh
└── tests/                        # Test files
    ├── test_credentials.py
    ├── test_file_operations.py
    ├── test_git_properties.py
    ├── test_https_properties.py
    └── test_service_restart.py
```

## Default Values Summary

| Variable              | Default Value                    |
|-----------------------|----------------------------------|
| LLM_MODEL             | ollama/deepseek-coder-v2:16b    |
| LLM_BASE_URL          | http://ollama:11434             |
| OLLAMA_HOST           | http://ollama:11434             |
| WORKSPACE_DIR         | /opt/workspace                  |
| OPENHANDS_WORKSPACE   | /opt/workspace                  |

## Validation

### Check Configuration
```bash
# View current environment variables
cat .env

# Test Ollama connection
curl http://localhost:11434/api/tags

# Test OpenHands UI
curl -I http://localhost:3000

# Verify Docker network
sudo docker network inspect ai-coding-network

# Check service status
sudo docker ps --format "table {{.Names}}\t{{.Status}}"
```

### Common Issues

**Issue**: Services can't communicate
- **Solution**: Verify all services are on `ai-coding-network`

**Issue**: Models not loading
- **Solution**: Check `OLLAMA_HOST` and `LLM_BASE_URL` match

**Issue**: GitHub integration not working
- **Solution**: Verify `GITHUB_TOKEN` is set and valid

**Issue**: Workspace not persisting
- **Solution**: Check volume mounts in docker-compose.yml

---
**Requirements Validated**: 10.2
**Last Updated**: 2025-11-29
