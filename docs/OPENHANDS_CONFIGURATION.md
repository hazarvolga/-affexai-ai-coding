# OpenHands Configuration Guide

## Overview
This guide explains how to configure OpenHands for optimal use with your AI Coding Platform, including AI model selection, MCP server setup, and advanced configurations.

## Table of Contents
1. [Accessing OpenHands](#accessing-openhands)
2. [AI Model Configuration](#ai-model-configuration)
3. [MCP Server Setup](#mcp-server-setup)
4. [GitHub Integration](#github-integration)
5. [Workspace Configuration](#workspace-configuration)
6. [Advanced Settings](#advanced-settings)

---

## Accessing OpenHands

### Web Interface
- **URL**: https://ai.fpvlovers.com.tr
- **Access**: Open in any modern web browser
- **No Login Required**: Direct access (unless authentication is configured)

### First Time Setup
1. Navigate to https://ai.fpvlovers.com.tr
2. You'll see the OpenHands chat interface
3. Start by typing a message to test the AI connection

---

## AI Model Configuration

### Available Models

Your system has two AI models installed:

#### 1. DeepSeek Coder V2 16B (Default)
- **Best for**: Complex coding tasks, large projects, detailed explanations
- **Speed**: Slower (more comprehensive)
- **Memory**: ~16GB RAM required
- **Quality**: Highest quality code generation

#### 2. Qwen2.5-Coder 7B
- **Best for**: Quick tasks, simple scripts, fast iterations
- **Speed**: Faster (2-3x faster than DeepSeek)
- **Memory**: ~8GB RAM required
- **Quality**: Good quality, efficient

### Switching Models

#### Method 1: Via Coolify (Recommended)

1. **Login to Coolify**
   ```
   https://coolify.fpvlovers.com.tr
   ```

2. **Navigate to Application**
   - Go to Projects → affexai-ai-coding
   - Click on "AI Coding Platform" application

3. **Update Environment Variables**
   - Click on "Environment Variables" tab
   - Find or add `LLM_MODEL` variable
   - Change value:
     - For DeepSeek: `ollama/deepseek-coder-v2:16b`
     - For Qwen: `ollama/qwen2.5-coder:7b`

4. **Restart Application**
   - Click "Restart" button
   - Wait for restart to complete (~30 seconds)

5. **Verify**
   - Go to https://ai.fpvlovers.com.tr
   - Ask the AI: "What model are you?"
   - It should respond with the model name

#### Method 2: Via SSH

```bash
# SSH into server
ssh ubuntu@161.118.171.201

# Edit environment (if using .env file)
nano ~/.env

# Change this line:
LLM_MODEL=ollama/qwen2.5-coder:7b

# Or update via Coolify API
# (Requires COOLIFY_API_TOKEN)

# Restart OpenHands
sudo docker restart openhands-kogccog8g0ok80w0kgcoc4ck-112840198537
```

### Model Comparison

| Feature | DeepSeek 16B | Qwen 7B |
|---------|--------------|---------|
| Response Time | 5-15 seconds | 2-5 seconds |
| Code Quality | Excellent | Good |
| Explanation Detail | Very detailed | Concise |
| Memory Usage | ~16GB | ~8GB |
| Best Use Case | Complex projects | Quick tasks |
| Context Window | 16K tokens | 32K tokens |

### Performance Tips

**For Better Performance:**
- Use Qwen for simple tasks and iterations
- Switch to DeepSeek for complex architecture decisions
- Monitor memory usage: `free -h`
- If system is slow, switch to Qwen

**Memory Management:**
```bash
# Check current memory usage
free -h

# If memory is high (>80%), restart Ollama
sudo docker restart ollama-kogccog8g0ok80w0kgcoc4ck-112840189768
```

---

## MCP Server Setup

### What are MCP Servers?

MCP (Model Context Protocol) servers extend OpenHands with additional capabilities like:
- File system access
- Database connections
- API integrations
- External tool access

### Installing MCP Servers

OpenHands supports MCP servers through its configuration. Here's how to set them up:

#### 1. File System MCP Server

Allows AI to read/write files in workspace:

```bash
# SSH into server
ssh ubuntu@161.118.171.201

# Create MCP config directory
mkdir -p ~/.openhands/mcp

# Create MCP config file
cat > ~/.openhands/mcp/config.json << 'EOF'
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/opt/workspace"],
      "env": {}
    }
  }
}
EOF
```

#### 2. GitHub MCP Server

Enhanced GitHub integration:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

#### 3. PostgreSQL MCP Server

Database access (if you have PostgreSQL):

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://user:pass@host:5432/db"
      }
    }
  }
}
```

#### 4. Web Search MCP Server

Allow AI to search the web:

```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "your_brave_api_key_here"
      }
    }
  }
}
```

### Complete MCP Configuration Example

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/opt/workspace"],
      "env": {}
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### Applying MCP Configuration

#### Via Docker Volume Mount

1. **Create config on server:**
   ```bash
   ssh ubuntu@161.118.171.201
   mkdir -p ~/openhands-config
   nano ~/openhands-config/mcp-config.json
   # Paste your MCP configuration
   ```

2. **Update Coolify to mount config:**
   - In Coolify, go to Application → Volumes
   - Add volume mount:
     - Host path: `/home/ubuntu/openhands-config`
     - Container path: `/root/.openhands/mcp`
   - Restart application

3. **Verify:**
   ```bash
   sudo docker exec openhands-kogccog8g0ok80w0kgcoc4ck-112840198537 \
     cat /root/.openhands/mcp/mcp-config.json
   ```

### Available MCP Servers

Popular MCP servers you can install:

| Server | Purpose | Package |
|--------|---------|---------|
| Filesystem | File operations | `@modelcontextprotocol/server-filesystem` |
| GitHub | GitHub API access | `@modelcontextprotocol/server-github` |
| PostgreSQL | Database queries | `@modelcontextprotocol/server-postgres` |
| Brave Search | Web search | `@modelcontextprotocol/server-brave-search` |
| Puppeteer | Browser automation | `@modelcontextprotocol/server-puppeteer` |
| Slack | Slack integration | `@modelcontextprotocol/server-slack` |

### Troubleshooting MCP

**MCP server not working:**
```bash
# Check OpenHands logs
sudo docker logs openhands-kogccog8g0ok80w0kgcoc4ck-112840198537 | grep -i mcp

# Verify Node.js is available in container
sudo docker exec openhands-kogccog8g0ok80w0kgcoc4ck-112840198537 node --version

# Test MCP server manually
sudo docker exec openhands-kogccog8g0ok80w0kgcoc4ck-112840198537 \
  npx -y @modelcontextprotocol/server-filesystem /opt/workspace
```

---

## GitHub Integration

### Setup GitHub Token

1. **Create Personal Access Token**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Set expiration: 90 days
   - Select scopes:
     - ✅ `repo` (all)
     - ✅ `workflow`
   - Generate and copy token

2. **Configure in Coolify**
   - Login to Coolify
   - Go to Application → Environment Variables
   - Add variable:
     - Name: `GITHUB_TOKEN`
     - Value: `ghp_your_token_here`
   - Save and restart

3. **Verify**
   ```bash
   # Test token
   curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user
   ```

### Using GitHub in OpenHands

Once configured, you can ask OpenHands to:

```
"Create a new GitHub repository called 'my-project'"
"Push this code to GitHub"
"Create a pull request with these changes"
"Clone repository https://github.com/user/repo"
```

---

## Workspace Configuration

### Workspace Structure

```
/opt/workspace/
├── projects/          # Your projects
│   ├── project-1/
│   ├── project-2/
│   └── ...
└── temp/             # Temporary files
```

### Accessing Workspace Files

#### Via OpenHands
- Files are automatically saved in workspace
- Ask: "Show me my projects"
- Ask: "List files in project-1"

#### Via SSH
```bash
# SSH into server
ssh ubuntu@161.118.171.201

# Access workspace
sudo ls -la /var/lib/docker/volumes/openhands-workspace/_data/

# Copy file from workspace
sudo cp /var/lib/docker/volumes/openhands-workspace/_data/projects/my-file.txt ~/
```

#### Via Docker
```bash
# Copy file from container
sudo docker cp openhands-kogccog8g0ok80w0kgcoc4ck-112840198537:/opt/workspace/projects/my-file.txt ./

# Copy file to container
sudo docker cp ./my-file.txt openhands-kogccog8g0ok80w0kgcoc4ck-112840198537:/opt/workspace/projects/
```

### Workspace Backup

```bash
# Backup workspace
sudo tar -czf workspace-backup-$(date +%Y%m%d).tar.gz \
  /var/lib/docker/volumes/openhands-workspace/_data/

# Restore workspace
sudo tar -xzf workspace-backup-YYYYMMDD.tar.gz -C /
```

---

## Advanced Settings

### Custom System Prompt

You can customize how OpenHands behaves:

1. **Create custom prompt file:**
   ```bash
   ssh ubuntu@161.118.171.201
   mkdir -p ~/openhands-config
   cat > ~/openhands-config/system-prompt.txt << 'EOF'
   You are an expert software engineer specializing in:
   - Clean, maintainable code
   - Test-driven development
   - Security best practices
   - Performance optimization
   
   Always:
   - Write comprehensive comments
   - Include error handling
   - Follow language-specific conventions
   - Suggest improvements
   EOF
   ```

2. **Mount in Coolify:**
   - Add volume: `~/openhands-config:/config`
   - Add environment variable: `SYSTEM_PROMPT_FILE=/config/system-prompt.txt`
   - Restart

### Resource Limits

Control OpenHands resource usage:

```bash
# In Coolify, set resource limits:
# Memory: 4GB
# CPU: 2 cores

# Or via docker-compose:
services:
  openhands:
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: '2'
```

### Logging Configuration

```bash
# Increase log verbosity
# In Coolify, add environment variable:
LOG_LEVEL=DEBUG

# View logs
sudo docker logs -f openhands-kogccog8g0ok80w0kgcoc4ck-112840198537

# Save logs to file
sudo docker logs openhands-kogccog8g0ok80w0kgcoc4ck-112840198537 > openhands.log
```

### Network Configuration

```bash
# Allow OpenHands to access external APIs
# Already configured via ai-coding-network

# Verify network
sudo docker network inspect ai-coding-network

# Test external connectivity
sudo docker exec openhands-kogccog8g0ok80w0kgcoc4ck-112840198537 \
  curl -I https://api.github.com
```

---

## Usage Examples

### Example 1: Create a Web Application

```
You: "Create a simple React todo app with TypeScript"

OpenHands will:
1. Create project structure
2. Set up package.json
3. Write React components
4. Add TypeScript types
5. Create README
```

### Example 2: Debug Code

```
You: "This function has a bug, can you fix it?"
[Paste your code]

OpenHands will:
1. Analyze the code
2. Identify the bug
3. Suggest fix
4. Explain the issue
```

### Example 3: Deploy to GitHub

```
You: "Create a GitHub repo and push this project"

OpenHands will:
1. Initialize git
2. Create .gitignore
3. Create GitHub repository
4. Push code
5. Provide repository URL
```

### Example 4: Write Tests

```
You: "Write unit tests for this function"
[Paste your function]

OpenHands will:
1. Analyze function
2. Write test cases
3. Include edge cases
4. Add test documentation
```

---

## Best Practices

### 1. Clear Instructions
```
❌ Bad: "Make it better"
✅ Good: "Refactor this function to use async/await instead of callbacks"
```

### 2. Provide Context
```
❌ Bad: "Fix the bug"
✅ Good: "This function should return an array but returns undefined. Here's the code: [paste code]"
```

### 3. Iterative Development
```
1. Start with basic structure
2. Add features incrementally
3. Test each feature
4. Refine based on results
```

### 4. Use Specific Commands
```
"Create a new file called utils.ts"
"Add error handling to the login function"
"Write a README with installation instructions"
"Generate TypeScript types for this API response"
```

---

## Troubleshooting

### OpenHands Not Responding

```bash
# Check if container is running
sudo docker ps | grep openhands

# Check logs
sudo docker logs --tail 100 openhands-kogccog8g0ok80w0kgcoc4ck-112840198537

# Restart
sudo docker restart openhands-kogccog8g0ok80w0kgcoc4ck-112840198537
```

### AI Responses Are Slow

```bash
# Switch to faster model (Qwen)
# In Coolify: LLM_MODEL=ollama/qwen2.5-coder:7b

# Check Ollama status
curl http://localhost:11434/api/tags

# Check memory
free -h
```

### Cannot Access Workspace Files

```bash
# Check permissions
sudo ls -la /var/lib/docker/volumes/openhands-workspace/_data/

# Fix permissions
sudo chown -R 1000:1000 /var/lib/docker/volumes/openhands-workspace/_data/
```

### GitHub Integration Not Working

```bash
# Verify token is set
sudo docker exec openhands-kogccog8g0ok80w0kgcoc4ck-112840198537 \
  env | grep GITHUB_TOKEN

# Test token
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user

# Update token in Coolify and restart
```

---

## Security Considerations

### 1. Token Security
- Never share your GitHub token
- Rotate tokens every 90 days
- Use minimal required permissions

### 2. Workspace Isolation
- Each project in separate directory
- Regular backups
- Monitor disk usage

### 3. Network Security
- OpenHands only accessible via HTTPS
- Internal services not exposed
- Firewall configured

### 4. Code Review
- Always review AI-generated code
- Test thoroughly before deployment
- Understand what the code does

---

## Quick Reference

### Essential Commands

```bash
# Check system health
bash ~/health-check-system.sh

# Restart OpenHands
sudo docker restart openhands-kogccog8g0ok80w0kgcoc4ck-112840198537

# View logs
sudo docker logs -f openhands-kogccog8g0ok80w0kgcoc4ck-112840198537

# Check Ollama models
curl http://localhost:11434/api/tags

# Backup workspace
sudo tar -czf workspace-backup.tar.gz /var/lib/docker/volumes/openhands-workspace/
```

### Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `LLM_MODEL` | AI model selection | `ollama/qwen2.5-coder:7b` |
| `LLM_BASE_URL` | Ollama endpoint | `http://ollama:11434` |
| `GITHUB_TOKEN` | GitHub access | `ghp_...` |
| `WORKSPACE_DIR` | Workspace path | `/opt/workspace` |

---

## Support

For issues or questions:
1. Check [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Review logs
3. Check system health
4. Contact system administrator

---

**Last Updated**: 2025-11-29
**OpenHands Version**: Latest
**Ollama Version**: Latest
